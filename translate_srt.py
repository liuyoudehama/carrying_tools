import re
import async_google_trans_new
import sys
import asyncio
import argparse

debug=False

async def translate_text_routine(text_list, index, translated_text_list, timeout=10, target_language='zh-cn'):
    asynctranslator = async_google_trans_new.AsyncTranslator()
    translated_text = '...'
    translation_success=False
    while not translation_success:
        try:
            async with asyncio.timeout(timeout):
                translated_text = await asynctranslator.translate(text_list[index], target_language)
        except:
            print(f"retrying translating:{text_list[index]}......")
        else:
            translation_success = True
    
    translated_text_list[index] = translated_text

def translate_text(text, target_language='zh-cn'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    if debug:
        print(f" before translated:{text}")
        print(f" after translated:{translation.text}")
    return translation.text

async def translate_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text_list = []
    
    for line in lines:
        # Check if the line is a timecode or subtitle
        if not re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line) \
            and not line.strip() == ''\
            and not re.match(r'\d+', line):
            text_list.append(line.strip())
    
    if debug:
        print(text_list)
    
    translated_list = [None] * len(text_list)

    async with asyncio.TaskGroup() as tg:
        for index in range(len(text_list)):
            task = tg.create_task(translate_text_routine(text_list, index, translated_list))
    
    if debug:
        print(translated_list)

    result_file_lines = []
    subtitle_cnt = 0
    for line in lines:
        # Check if the line is a timecode or subtitle
        if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
            # Timecode line, keep it unchanged
            result_file_lines.append(line)
        elif line.strip() == '':
            # Empty line, keep it unchanged
            result_file_lines.append(line)
        elif re.match(r'\d+', line):
            # number line, keep it.
            result_file_lines.append(line)
        else:
            # Append both original and translated lines
            result_file_lines.append(text_list[subtitle_cnt])
            result_file_lines.append('\n')
            result_file_lines.append(translated_list[subtitle_cnt])
            result_file_lines.append('\n')
            subtitle_cnt += 1

    if debug:
        print(result_file_lines)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(''.join(result_file_lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="translator")
    parser.add_argument("--input", type=str, help="input srt", required=True)
    parser.add_argument("--output", type=str, help="output srt", required=True)
    args = parser.parse_args()
    input_srt_file = args.input
    output_srt_file = args.output
    asyncio.run(translate_srt(input_srt_file, output_srt_file))
