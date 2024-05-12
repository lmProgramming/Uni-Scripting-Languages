import os
import subprocess

def analyze_text_file(file_path):
    result = subprocess.run(["C:/Users/janta/source/repos/Text Analyzer 2/Text Analyzer 2/bin/Debug/net5.0/TextAnalyzer.exe", 
                             file_path], capture_output=True, text=True)
    
    lines = result.stdout.strip().split('\n')
    data = {}
    
    keys = lines[0].split(",")
    values = []
    for line in lines:
        values = line.split(',')
        
        for value, key in zip(values, keys):
            data[key] = value.strip()

    return data

def main(directory_path):
    results = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):            
            file_path = os.path.join(directory_path, filename)
            file_data = analyze_text_file(file_path)

            results.append(file_data)
            
    process_outputs(results)
    
def process_outputs(results):
    total_files = len(results)
    total_characters = 0
    total_words = 0
    total_lines = 0
    character_frequency = {}
    word_frequency = {}   

    most_common_char = max(character_frequency, key=character_frequency.get)

    most_common_word = max(word_frequency, key=word_frequency.get)
    
    for result in results:

        total_characters += int(result['char count'])
        total_words += int(result['word count'])
        total_lines += int(result['line count'])

        most_common_char = result['most common char']
        if most_common_char in character_frequency:
            character_frequency[most_common_char] += 1
        else:
            character_frequency[most_common_char] = 1

        most_common_word = result['most common word']
        if most_common_word in word_frequency:
            word_frequency[most_common_word] += 1
        else:
            word_frequency[most_common_word] = 1           
    
    print("Liczba przeczytanych plików:", total_files)
    print("Sumaryczna liczba znaków:", total_characters)
    print("Sumaryczna liczba słów:", total_words)
    print("Sumaryczna liczba wierszy:", total_lines)
    print("Znak występujący najczęściej:", most_common_char)
    print("Słowo występujące najczęściej:", most_common_word)

if __name__ == "__main__":
    directory_path = input("Podaj ścieżkę do katalogu z plikami tekstowymi: ")
    main(directory_path)