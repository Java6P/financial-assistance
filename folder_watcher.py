import os
import re
import time
from datetime import datetime


class FolderWatcher:
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.processed_files = set()
        self._init_processed_files()
    
    def _init_processed_files(self):
        if os.path.exists(self.watch_dir):
            for file_name in os.listdir(self.watch_dir):
                if file_name.endswith('.txt'):
                    self.processed_files.add(file_name)
    
    def process_file(self, file_name):
        file_path = os.path.join(self.watch_dir, file_name)
        
        if file_name.startswith('done_'):
            return
        
        print(f"[INFO] 检测到新文件: {file_name}")
        
        try:
            time.sleep(0.5)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            number_pattern = r'-?\d+(?:\.\d+)?'
            numbers = re.findall(number_pattern, content)
            total = 0.0
            for num in numbers:
                try:
                    total += float(num)
                except ValueError:
                    continue
            
            result = str(int(total)) if total == int(total) else str(total)
            print(f"[INFO] 提取的数字: {numbers}")
            print(f"[INFO] 求和结果: {result}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_file_name = f'done_{timestamp}.txt'
            new_file_path = os.path.join(self.watch_dir, new_file_name)
            
            os.rename(file_path, new_file_path)
            self.processed_files.add(new_file_name)
            print(f"[INFO] 文件已重命名为: {new_file_name}")
            print("-" * 50)
            
        except Exception as e:
            print(f"[ERROR] 处理文件 {file_name} 时出错: {e}")
    
    def run(self):
        if not os.path.exists(self.watch_dir):
            os.makedirs(self.watch_dir)
            print(f"[INFO] 创建监控文件夹: {self.watch_dir}")
        
        print(f"[INFO] 开始监控文件夹: {self.watch_dir}")
        print("[INFO] 等待新的 .txt 文件...")
        print("-" * 50)
        
        try:
            while True:
                current_files = set()
                
                if os.path.exists(self.watch_dir):
                    for file_name in os.listdir(self.watch_dir):
                        if file_name.endswith('.txt'):
                            current_files.add(file_name)
                
                new_files = current_files - self.processed_files
                for file_name in new_files:
                    if not file_name.startswith('done_'):
                        self.process_file(file_name)
                
                self.processed_files = current_files
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n[INFO] 监控已停止")


def main():
    watch_dir = 'D:/test_watch'
    watcher = FolderWatcher(watch_dir)
    watcher.run()


if __name__ == '__main__':
    main()
