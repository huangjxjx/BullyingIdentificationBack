# audio_worker.py

import json
import os
import numpy as np
import soundfile as sf
import tensorflow_hub as hub
import tensorflow as tf
from vosk import Model as VoskModel, KaldiRecognizer
from modelscope import pipeline, Tasks
from datetime import datetime

SAMPLE_RATE = 16000
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
vosk_model = VoskModel(r"D:\Program Files\PyCharmProject\app\api\model")
recognizer = KaldiRecognizer(vosk_model, SAMPLE_RATE)
emotion_model = pipeline(
    task=Tasks.emotion_recognition,
    model="iic/emotion2vec_base_finetuned"
)

# 加载YAMNet类标签
class_map_path = tf.keras.utils.get_file(
    'yamnet_class_map.csv',
    'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
)
class_names = [line.strip().split(',')[2] for line in open(class_map_path).readlines()[1:]]

BULLYING_KEYWORDS = [
    "你去死", "滚开", "闭嘴", "废物", "没用", "白痴", "蠢货", "傻逼", "垃圾", "打你", "揍你",
    "混蛋", "王八蛋", "婊子", "臭不要脸", "贱人", "草你", "妈的", "滚蛋"
]

ALERT_LABELS = ["scream", "cry", "sob", "yell", "shout", "smack", "slap", "slam"]

def is_bullying_text(text, user_keywords=None):
    # 合并系统默认关键词 + 用户自定义关键词
    custom_keywords = [kw.keyword for kw in user_keywords] if user_keywords else []
    full_keywords = BULLYING_KEYWORDS + custom_keywords
    return [kw for kw in full_keywords if kw in text]

def analyze_yamnet(block):
    scores, _, _ = yamnet_model(block)
    mean_scores = scores.numpy().mean(axis=0)
    top_idx = np.argsort(mean_scores)[-5:][::-1]

    top_results = [(class_names[i], float(mean_scores[i])) for i in top_idx]

    # 判断是否有危险事件
    danger_events = [item for item in top_results if any(k in item[0].lower() for k in ALERT_LABELS)]

    if danger_events:
        return danger_events[0], True  # 返回事件 + 是危险的
    else:
        return top_results[0], False   # 返回事件 + 非危险


def analyze_emotion(block):
    temp_path = "temp_emotion.wav"
    sf.write(temp_path, block, SAMPLE_RATE)
    try:
        result = emotion_model(temp_path, granularity="utterance")
        if result:
            # 选置信度最高的情绪
            labels = result[0]['labels']
            scores = result[0]['scores']
            max_idx = int(np.argmax(scores))
            label_full = labels[max_idx]
            score = scores[max_idx]
            label = label_full.split("/")[-1].lower()
            return label, float(score)
    except Exception as e:
        print("emotion error:", e)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return "unknown", 0.0


def analyze_block(block, user_keywords=None):
    result = {
        "timestamp": datetime.now().isoformat(),
        "text": "",
        "keywords": [],
        "events": [],
        "emotion": None
    }

    # VOSK 语音识别
    audio_bytes = (block * 32767).astype(np.int16).tobytes()
    if recognizer.AcceptWaveform(audio_bytes):
        text = json.loads(recognizer.Result()).get("text", "")
        result["text"] = text
        result["keywords"] = is_bullying_text(text, user_keywords)

    # YAMNet 危险声音检测
    block_mono = np.squeeze(block)
    event_info, is_danger_event = analyze_yamnet(block_mono)
    result["events"] = [{"label": event_info[0], "score": event_info[1]}]
    result["is_danger_event"] = is_danger_event

    # Emotion2Vec 情绪识别
    label, score = analyze_emotion(block)
    if label:
        result["emotion"] = {"label": label, "score": score}

    return result
