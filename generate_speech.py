#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import av
import json
import shutil
import subprocess

from pydub import AudioSegment

# 可以修改的默认配置
video_file      = "media/videos/template/480p15/Template.mp4"
subtitles_file  = "media/subtitles.jsonl"
voice_name      = "longlaotie" # 可选 "loongbella" 或 "longmiao" 等

# 一般不修改的默认配置
cache_dir       = "media/audio"


def tts_engine_aliyun(text, mp3_file, role="longmiao"):
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
    
    model = "cosyvoice-v1"
    voice = role
    # 从系统环境变量中获取阿里云API密钥
    dashscope.api_key = os.environ.get("ALIYUNAPI", "")

    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call(text)

    with open(mp3_file, 'wb') as f:
        f.write(audio)

    audio_duration = get_audio_duration(mp3_file)
    print(f"生成的语音时长: {audio_duration:.2f}秒")

    return audio_duration


def read_subtitles(subtitle_file):
    """读取字幕文件"""
    # 读取第一行获取视频文件和音色信息
    with open(subtitle_file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        try:
            config = json.loads(first_line)
            global video_file, voice_name
            video_file = config.get("video_file", video_file)
            voice_name = config.get("voice_name", voice_name)
        except json.JSONDecodeError:
            print("警告: 字幕文件第一行不是配置信息！")
            exit(1)
    
    subtitles = []
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            next(f)  # 跳过第一行
            for line in f:
                subtitles.append(json.loads(line))
        print(f"已读取 {len(subtitles)} 条字幕")
        return video_file, voice_name, subtitles
    except FileNotFoundError:
        print(f"错误: 找不到字幕文件 {subtitle_file}")
        return []
    except json.JSONDecodeError:
        print(f"错误: 字幕文件 {subtitle_file} 格式不正确")
        return []

def run_tts_4all(subtitles, voice_name):
    """生成所有语音并返回文件列表和时长列表，主程序需要用它来调节动画时间"""

    N = len(subtitles)
    print(f"开始处理 {N} 条字幕...")
    
    # 生成所有语音
    file_list, duration_list = [], []
    for i in range(N):
        sub = subtitles[i]
        audio_file = os.path.join(cache_dir, f"audio_{i:03d}.mp3")
        print(f"\n处理字幕 {i+1}/{N}: '{sub['text']}'")

        # 生成语音并记录时长
        duration = tts_engine_aliyun(sub['text'], audio_file, voice_name)
        
        # 记录文件路径和时长
        file_list.append(audio_file)
        duration_list.append(duration)
    
    return file_list, duration_list


def make_final_audio(subtitles, audio_files, total_duration):
    """根据总时间创建空白音频，并根据字幕指定的时间插入每个字幕的语音（已经生成好的）"""
    
    full_audio_file = os.path.join(cache_dir, "full_audio.mp3")

    # 创建空白音频，时间单位为 ms
    full_audio = AudioSegment.silent(duration=int(total_duration * 1000))

    # 插入每个字幕的语音
    N = len(subtitles)
    for i in range(N):
        sub, audio_file = subtitles[i], audio_files[i]

        segment = AudioSegment.from_mp3(audio_file)
        position = int(sub['start_time'] * 1000)  # 毫秒
        
        full_audio = full_audio.overlay(segment, position=position)
        print(f"已添加音频: '{sub['text']}' 在 {sub['start_time']:.2f}秒处")
    
    # 导出完整音频
    full_audio.export(full_audio_file, format="mp3")
    
    print(f"已生成完整配音文件: {full_audio_file} (总时长: {total_duration:.2f}秒)")


def get_video_duration(video_file):
    """使用 pyav 获取视频时长"""
    try:
        # 打开视频文件
        container = av.open(video_file)
        
        # 获取视频时长（以秒为单位）
        video_duration = float(container.duration / av.time_base)
        
        # 关闭容器
        container.close()
        
        return video_duration
    except Exception as e:
        print(f"获取视频时长时出错: {e}")
        return False

def get_audio_duration(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    return audio.duration_seconds


def verify_time(video_file):
    """验证视频和音频的同步性"""
    
    full_audio_file = os.path.join(cache_dir, "full_audio.mp3")
    
    video_duration = get_video_duration(video_file)
    audio_duration = get_audio_duration(full_audio_file)
    
    # 比较时长（允许0.5秒的误差）
    duration_diff = abs(video_duration - audio_duration)
    is_synced = duration_diff <= 0.5
    
    print(f"同步验证结果:")
    print(f"  视频时长: {video_duration:.2f}秒")
    print(f"  音频时长: {audio_duration:.2f}秒")
    print(f"  时长差异: {duration_diff:.2f}秒")
    print(f"  同步状态: {'可以认为成功' if is_synced else '有可能失败，请检查'}")
    
    return is_synced

def merge_video_audio(video_file, verbose=True):
    """合并视频和音频
    Args:
        video_file: 视频文件路径
        verbose: 是否显示ffmpeg输出，默认为True
    """
    full_audio_file = os.path.join(cache_dir, "full_audio.mp3")

    # 使用ffmpeg合并视频和音频
    output_file = video_file.replace('.mp4', '_WithAudio.mp4')
    cmd = [
        'ffmpeg',
        '-i', video_file,
        '-i', full_audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_file,
        '-y'  # 覆盖已存在的文件
    ]
    
    try:
        print(f"正在合并视频和音频...")
        # 根据verbose参数决定是否显示ffmpeg输出
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL if not verbose else None, stderr=subprocess.DEVNULL if not verbose else None)
        print(f"合并完成: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"合并视频和音频时出错: {e}")
        return False


def clean_cache(cache_dir):
    shutil.rmtree(cache_dir, ignore_errors=True)
    print("已清理临时文件")


def generate_speech(subtitles_file, verbose=False):
    os.makedirs(cache_dir, exist_ok=True)

    # 读取字幕文件，其中包含字幕的编号、开始时间、文本内容
    video_file, voice_name, subtitles = read_subtitles(subtitles_file)

    print(f"开始生成语音，使用音色：{voice_name}")
    print(f"视频文件：{video_file}")
    print(f"字幕文件：{subtitles_file}")

    # 对所有字幕生成语音
    audio_files, duration_list = run_tts_4all(subtitles, voice_name)

    # 计算视频文件的总长度
    total_time = get_video_duration(video_file)
    
    # 根据字幕的开始时间，将语音插入到完整音频中
    make_final_audio(subtitles, audio_files, total_time)
    
    # 验证视频和音频的同步性
    verify_time(video_file)
    
    # 合并视频和音频
    merge_video_audio(video_file, verbose)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成语音")
    parser.add_argument("subtitle_file", type=str, help="字幕文件路径")
    args = parser.parse_args()
    subtitles_file = args.subtitle_file

    generate_speech(subtitles_file)
