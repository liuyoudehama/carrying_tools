import subprocess
import argparse
import copy
import time
import argparse

download_command = ["youtube-dl",\
					 "-f",\
					 "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",\
					]


def read_downloading_list(input_file :str = 'input.txt')->list:
	with open(input_file, 'r') as file:
		lines = file.readlines()
		return lines
	
def download_from(input_file: str, max_process=20):
	source_list = read_downloading_list(input_file)
	
	print("source_list:")
	print(source_list)
	
	process_list = []
	max_process_cnt = max_process
	last_waiting_cnt = 0

	while len(source_list) > 0 or len(process_list) > 0:
		if len(source_list) > 0 and len(process_list) < max_process_cnt:
			process_command = copy.deepcopy(download_command)
			process_command.append(source_list[0])
			source_list.remove(source_list[0])
			
			print(f'spawn {process_command}')
			process = subprocess.Popen(process_command)
			print("Process Command:", " ".join(process.args))

			process_list.append(process)
		else:
			free_cnt = 0
			for process in process_list:
				if process.poll() is not None:
					process_list.remove(process)
					free_cnt += 1
			if free_cnt == 0:
				if last_waiting_cnt != len(source_list):
					print(f"{len(source_list)} is awaiting......")
					last_waiting_cnt = len(source_list)
				time.sleep(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="downloader")
	parser.add_argument("--input", type=str, help="input file path")
	args = parser.parse_args()
	input_file = args.input
	download_from(input_file)