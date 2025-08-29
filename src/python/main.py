#!/usr/bin/env python3

import sys
import time
import threading
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from web_api.app import create_app
from image_processing.fermentation_analyzer import FermentationAnalyzer
from data_storage.database import Database

class FermentationMonitor:
    def __init__(self):
        self.db = Database()
        self.image_analyzer = FermentationAnalyzer()
        self.running = False
        
    def start_monitoring(self):
        self.running = True
        
        # Start image analysis thread for dough size monitoring
        image_thread = threading.Thread(target=self._monitor_dough_size)
        image_thread.daemon = True
        image_thread.start()
        
        # Start web server
        app = create_app(self.db)
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    def stop_monitoring(self):
        self.running = False
        
    def _monitor_dough_size(self):
        while self.running:
            try:
                # Capture and analyze dough size from webcam
                metrics = self.image_analyzer.analyze()
                if metrics:
                    self.db.store_image_metrics(metrics)
                    print(f"Dough size: {metrics.get('size', 'N/A')}")
                    
            except Exception as e:
                print(f"Dough monitoring error: {e}")
                
            time.sleep(300)  # Analyze dough size every 5 minutes

if __name__ == "__main__":
    monitor = FermentationMonitor()
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        monitor.stop_monitoring()
        print("Fermentation monitor stopped")