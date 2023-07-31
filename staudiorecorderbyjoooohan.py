#使用这个录音模块：https://pypi.org/project/audio-recorder-streamlit/
import streamlit as st
import subprocess
import openai
#import pyttsx3
#import sounddevice as sd
import soundfile as sf
import numpy as np
from audio_recorder_streamlit import audio_recorder
import numpy as np
#运行的时候有报错sh:1: ffmpeg not found
import ffmpeg
import av
#from pydub import AudioSegment
# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are an intelligent professor."}]

st.title("by Joohan Audio to Chat App")

    # Audio input section
st.header("Step 1: Speak to the AI")
st.write("Click the Record Button below and speak to the AI.")

audio = audio_recorder()

if len(audio) > 0:
    # To play audio in frontend:
    st.write("你输入的语音")
    st.audio(audio.tobytes())    
    # To save audio to a file:/可以视为是临时文件，就是用于语音转文本用
#Open file "audiorecorded.mp3" in binary write mode
#    audio_file = open("audiorecorded.webm", "wb")    
    audio_file = open("audiorecorded.mp3", "wb")
    audio_file.write(audio.tobytes())
    audio_file.close()

with open("audiorecorded.mp3", "rb") as sst_audio_file:
    transcript = openai.Audio.transcribe(
        file = sst_audio_file,
        model = "whisper-1",
        response_format="text"        
    )
    print(transcript)
    st.write(transcript)

#if audio_bytes:
#    st.audio(audio_bytes, format="audio/wav")    

# Save the audio data to a WAV file
#****************更换下面的语音转文字代码，主要是转化录音的格式
    # Convert the audio data to a numpy array with one channel (mono)

# Assume data is a tuple containing the audio data for a single-channel audio
#audio_file = "justnameit.wav"
#if len(audio_bytes) > 0:
#    audio_data = audio_bytes[0]  # Access the first element for a single-channel audio
#    sf.write(audio_file, audio_data, 44100, format="wav")
#else:
#    print("Error: The audio data （audio_bytes） is empty.")

#audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
#audio_file = "justnameit.wav"
#sf.write(audio_file, audio_bytes, 44100, format="wav")

    # Transcribe the audio using OpenAI API
#with open(audio_file, "rb") as file:
#    transcript = openai.Audio.transcribe("whisper-1", file)
#    return transcript["text"]    
#    text = transcript["text"]    
            # Remove the temporary audio file
#    os.remove(audio_file)    
#****************

    # Print the transcript
    print("Transcript of your questions:",  transcript)
#    print("Transcript of your questions:",  transcript["text"])

#   ChatGPT API
#   append user's inut to conversation
    conversation.append({"role": "user", "content": transcript})
#    conversation.append({"role": "user", "content": transcript["text"]})
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation
    )    
    print(response)

#   system_message is the response from ChatGPT API
    system_message = response["choices"][0]["message"]["content"]

#   append ChatGPT response (assistant role) back to conversation
    conversation.append({"role": "assistant", "content": system_message})

# Display the chat history
    st.header("你和AI的问答文字记录")
    st.write("你的提问（语音转文字）: " + transcript)
#    st.write("你的提问（语音转文字）: " + transcript["text"])
    st.write("AI回答（文字）: " + system_message)
    st.header("第二步：语音播放AI的回答")

language = detect(system_message)

st.write("检测到输出语言:", language)
print(language)

def text_to_speech(text):
    try:
        tts = gTTS(text, lang=language, slow=False)
        tts.save("translationresult.mp3")
        st.write("Success TTS成功将AI回答转换为语音")
        return "Success TTS成功将AI回答转换为语音"    
    except Exception as e:
        # Handle the error, e.g., print an error message or return a default text
        print(f"Translation error: {e}")
        st.write("TTS RESULT ERROR将AI回答转语音失败！")
        return "TTS RESULT ERROR将AI回答转语音失败！"
        st.stop()

if system_message is None:
    st.write("请先向AI提问！")    
    st.stop()
else: 
    st.write("你的提问（AI问答模型中的记录transcript）")
    st.write(transcript)
    st.write("AI回答")            
    ai_output_audio = text_to_speech(system_message)
    audio_file = open("translationresult.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio("translationresult.mp3")
    st.write(response)    
    st.write(system_message)    
