#imports.
import openai
from pathlib import Path

# api key.
openai.api_key ="your_key"

user_input=input("paste your text here: ")

res_summary = openai.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": f'summarize: {user_input}'},
    ],
    max_tokens = 150
)

summary = res_summary.choices[0].message.content

res_keywords = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": f"important keywords from: {user_input}"},
    ],
    max_tokens = 50
)
res_image_sub = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": f"generate one subject from the text which can be used as prompt for generating image: {user_input}"},
    ],
    max_tokens = 50
)

image_subjects = res_image_sub.choices[0].message.content

keywords = res_keywords.choices[0].message.content
print(f'Summary: {summary}')
print(f'keywords: {keywords}')
print(f"Image Subjects: {image_subjects}")

res_images = openai.images.generate(
  model="dall-e-3",
  prompt=f"{image_subjects}",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = res_images.data[0].url
print(image_url)

file_path = Path(__file__).parent / 'speech.mp3'
response = openai.audio.speech.create(
    model='tts-1',
    voice='nova',
    input=f'{summary}'
)
response.stream_to_file(file_path)

