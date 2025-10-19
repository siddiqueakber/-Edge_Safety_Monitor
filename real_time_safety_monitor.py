"""
Real-Time Safety Monitoring System
Detects PPE compliance in real-time from webcam or video files
Monitors: Hardhat, Mask, Safety Vest, Machinery, Vehicles
Classes: Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, Machinery, Vehicle
"""

from ultralytics import YOLO
import cv2
from datetime import datetime
from pathlib import Path
import argparse

class SafetyMonitor:
    def __init__(self, model_path, conf_threshold=0.5):
        """Initialize the safety monitoring system"""
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        
        # PPE compliance tracking
        self.violations = {
            'frames_processed': 0,
            'violations_detected': 0,
            'hardhat_detections': 0,
            'mask_detections': 0,
            'safety_vest_detections': 0,
            'no_hardhat_detections': 0,
            'no_mask_detections': 0,
            'no_vest_detections': 0,
            'person_detections': 0,
            'safety_cone_detections': 0,
            'machinery_detections': 0,
            'vehicle_detections': 0
        }
        
        # Create outputs directory
        self.output_dir = Path("outputs/safety_monitoring")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Safety Monitor Initialized")
        print(f"📊 Model: {model_path}")
        print(f"🎯 Classes: {self.model.names}")
        print(f"⚠️  Confidence Threshold: {conf_threshold}")
        print(f"👷 Monitoring PPE: Hardhat, Mask, Safety Vest, Machinery, Vehicles")
    
    def detect_violations(self, frame):
        """Detect PPE compliance violations in a frame"""
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        
        # Track detections in this frame
        detections = {
            'hardhat': 0,
            'mask': 0,
            'safety_vest': 0,
            'no_hardhat': 0,
            'no_mask': 0,
            'no_vest': 0,
            'person': 0,
            'safety_cone': 0,
            'machinery': 0,
            'vehicle': 0
        }
        
        violations_found = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls].lower()
                
                # Track all detections - normalize label names
                if 'hardhat' in label and 'no' not in label:
                    detections['hardhat'] += 1
                    self.violations['hardhat_detections'] += 1
                elif 'mask' in label and 'no' not in label:
                    detections['mask'] += 1
                    self.violations['mask_detections'] += 1
                elif 'safety vest' in label and 'no' not in label:
                    detections['safety_vest'] += 1
                    self.violations['safety_vest_detections'] += 1
                elif 'no' in label and 'hardhat' in label:
                    detections['no_hardhat'] += 1
                    self.violations['no_hardhat_detections'] += 1
                    violations_found.append({'type': 'no_hardhat', 'confidence': conf})
                elif 'no' in label and 'mask' in label:
                    detections['no_mask'] += 1
                    self.violations['no_mask_detections'] += 1
                    violations_found.append({'type': 'no_mask', 'confidence': conf})
                elif 'no' in label and 'vest' in label:
                    detections['no_vest'] += 1
                    self.violations['no_vest_detections'] += 1
                    violations_found.append({'type': 'no_vest', 'confidence': conf})
                elif 'person' in label:
                    detections['person'] += 1
                    self.violations['person_detections'] += 1
                elif 'safety cone' in label or 'cone' in label:
                    detections['safety_cone'] += 1
                    self.violations['safety_cone_detections'] += 1
                elif 'machinery' in label:
                    detections['machinery'] += 1
                    self.violations['machinery_detections'] += 1
                elif 'vehicle' in label:
                    detections['vehicle'] += 1
                    self.violations['vehicle_detections'] += 1
        
        return results, violations_found, detections
    
    def draw_violations(self, frame, results, violations, detections):
        """Draw bounding boxes and violation warnings with professional layout"""
        # Draw detections with bounding boxes
        annotated = results[0].plot()
        
        # Check for safety violations
        has_violations = len(violations) > 0
        
        # ===== TOP BANNER - STATUS =====
        banner_height = 140
        cv2.rectangle(annotated, (0, 0), (annotated.shape[1], banner_height), 
                     (0, 0, 255) if has_violations else (0, 180, 0), -1)
        
        # Status text
        status_text = "⚠️  VIOLATION DETECTED" if has_violations else "✅ SAFETY COMPLIANT"
        status_color = (255, 255, 255)
        cv2.putText(annotated, status_text, (15, 35), 
                   cv2.FONT_HERSHEY_DUPLEX, 1.2, status_color, 2)
        
        # Details line 1
        details1 = f"Workers: {detections['person']} | Hardhats: {detections['hardhat']} | Masks: {detections['mask']} | Vests: {detections['safety_vest']}"
        cv2.putText(annotated, details1, (15, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 1)
        
        # Violations line
        if has_violations:
            violations_text = f"Violations: No-Hat({detections['no_hardhat']}) | No-Mask({detections['no_mask']}) | No-Vest({detections['no_vest']})"
            cv2.putText(annotated, violations_text, (15, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 1)
        else:
            cv2.putText(annotated, "All workers compliant with safety requirements", (15, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 1)
        
        # ===== BOTTOM INFO BAR =====
        info_height = 60
        cv2.rectangle(annotated, (0, annotated.shape[0] - info_height), 
                     (annotated.shape[1], annotated.shape[0]), (40, 40, 40), -1)
        
        # Other detections info
        other_info = f"🚧 Cones: {detections['safety_cone']} | ⚙️ Machinery: {detections['machinery']} | 🚗 Vehicles: {detections['vehicle']}"
        cv2.putText(annotated, other_info, (15, annotated.shape[0] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(annotated, timestamp, (annotated.shape[1] - 250, annotated.shape[0] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return annotated
    
    def monitor_webcam(self):
        """Monitor safety from webcam feed"""
        print("\n🎥 Starting Webcam Monitoring...")
        print("Press 'q' to quit, 's' to save snapshot")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            # Detect violations
            results, violations, detections = self.detect_violations(frame)
            self.violations['frames_processed'] += 1
            
            if violations:
                self.violations['violations_detected'] += 1
            
            # Draw results
            annotated = self.draw_violations(frame, results, violations, detections)
            
            # Display
            cv2.imshow('Safety Monitor - Press Q to quit', annotated)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Save snapshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.output_dir / f"snapshot_{timestamp}.jpg"
                cv2.imwrite(str(filename), annotated)
                print(f"📸 Snapshot saved: {filename}")
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Print summary
        compliance_rate = ((self.violations['frames_processed'] - self.violations['violations_detected']) / self.violations['frames_processed'] * 100) if self.violations['frames_processed'] > 0 else 0
        print("\n" + "="*70)
        print("📊 MONITORING SESSION SUMMARY")
        print("="*70)
        print(f"Total Frames Processed: {self.violations['frames_processed']}")
        print(f"Violation Frames: {self.violations['violations_detected']}")
        print(f"Safety Compliance Rate: {compliance_rate:.2f}%")
        print(f"\nPPE Detections Summary:")
        print(f"  👷 Hardhats: {self.violations['hardhat_detections']}")
        print(f"  😷 Masks: {self.violations['mask_detections']}")
        print(f"  🦺 Safety Vests: {self.violations['safety_vest_detections']}")
        print(f"\nViolations Detected:")
        print(f"  ❌ No-Hardhat: {self.violations['no_hardhat_detections']}")
        print(f"  ❌ No-Mask: {self.violations['no_mask_detections']}")
        print(f"  ❌ No-Safety Vest: {self.violations['no_vest_detections']}")
        print(f"\nOther Detections:")
        print(f"  👤 Persons: {self.violations['person_detections']}")
        print(f"  🚧 Safety Cones: {self.violations['safety_cone_detections']}")
        print(f"  ⚙️ Machinery: {self.violations['machinery_detections']}")
        print(f"  🚗 Vehicles: {self.violations['vehicle_detections']}")
        print("="*70)
    
    def monitor_video(self, video_path):
        """Monitor safety from video file"""
        print(f"\n🎥 Processing Video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open video file: {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Setup video writer
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"monitored_{timestamp}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        print(f"📹 Video Properties: {width}x{height} @ {fps}fps, {total_frames} frames")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Detect violations
            results, violations, detections = self.detect_violations(frame)
            self.violations['frames_processed'] += 1
            
            if violations:
                self.violations['violations_detected'] += 1
            
            # Draw results
            annotated = self.draw_violations(frame, results, violations, detections)
            
            # Write frame
            out.write(annotated)
            
            # Progress indicator
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames * 100)
                print(f"Processing... {frame_count}/{total_frames} frames ({progress:.1f}%)", end='\r')
        
        cap.release()
        out.release()
        
        # Print summary
        compliance_rate = ((self.violations['frames_processed'] - self.violations['violations_detected']) / self.violations['frames_processed'] * 100) if self.violations['frames_processed'] > 0 else 0
        print("\n" + "="*70)
        print("📊 VIDEO PROCESSING SUMMARY")
        print("="*70)
        print(f"Video Saved: {output_path}")
        print(f"Total Frames Processed: {self.violations['frames_processed']}")
        print(f"Violation Frames: {self.violations['violations_detected']}")
        print(f"Safety Compliance Rate: {compliance_rate:.2f}%")
        print(f"\nPPE Detections Summary:")
        print(f"  👷 Hardhats: {self.violations['hardhat_detections']}")
        print(f"  😷 Masks: {self.violations['mask_detections']}")
        print(f"  🦺 Safety Vests: {self.violations['safety_vest_detections']}")
        print(f"\nViolations Detected:")
        print(f"  ❌ No-Hardhat: {self.violations['no_hardhat_detections']}")
        print(f"  ❌ No-Mask: {self.violations['no_mask_detections']}")
        print(f"  ❌ No-Safety Vest: {self.violations['no_vest_detections']}")
        print(f"\nOther Detections:")
        print(f"  👤 Persons: {self.violations['person_detections']}")
        print(f"  🚧 Safety Cones: {self.violations['safety_cone_detections']}")
        print(f"  ⚙️ Machinery: {self.violations['machinery_detections']}")
        print(f"  🚗 Vehicles: {self.violations['vehicle_detections']}")
        print("="*70)
    
    def monitor_image(self, image_path):
        """Monitor safety in a single image"""
        print(f"\n📸 Processing Image: {image_path}")
        
        # Read image
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"❌ Error: Could not read image: {image_path}")
            return
        
        # Detect violations
        results, violations, detections = self.detect_violations(frame)
        
        # Draw results
        annotated = self.draw_violations(frame, results, violations, detections)
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"result_{timestamp}.jpg"
        cv2.imwrite(str(output_path), annotated)
        
        # Print summary
        print("="*70)
        print("📊 IMAGE DETECTION SUMMARY")
        print("="*70)
        print(f"Detections:")
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls]
                print(f"  - {label.upper()}: {conf*100:.1f}% confidence")
        
        print(f"\nPPE Summary:")
        print(f"  👷 Hardhats: {detections['hardhat']}")
        print(f"  😷 Masks: {detections['mask']}")
        print(f"  🦺 Safety Vests: {detections['safety_vest']}")
        print(f"  👤 Persons: {detections['person']}")
        print(f"\nViolations:")
        print(f"  ❌ No-Hardhat: {detections['no_hardhat']}")
        print(f"  ❌ No-Mask: {detections['no_mask']}")
        print(f"  ❌ No-Safety Vest: {detections['no_vest']}")
        
        if violations:
            print(f"\n⚠️  SAFETY VIOLATIONS DETECTED: {len(violations)}")
        else:
            print(f"\n✅ All workers compliant with safety requirements")
        
        print(f"\n💾 Result saved: {output_path}")
        print("="*70)


def main():
    parser = argparse.ArgumentParser(description='Real-Time Safety Monitoring System')
    parser.add_argument('--model', type=str, default='models/ppe_detection_4classes/best.pt',
                       help='Path to trained PPE detection model')
    parser.add_argument('--source', type=str, default='webcam',
                       help='Source: "webcam", video file path, or image file path')
    parser.add_argument('--conf', type=float, default=0.5,
                       help='Confidence threshold (0.0-1.0)')
    
    args = parser.parse_args()
    
    # Initialize monitor
    monitor = SafetyMonitor(args.model, args.conf)
    
    # Process based on source type
    if args.source.lower() == 'webcam':
        monitor.monitor_webcam()
    elif Path(args.source).suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        monitor.monitor_video(args.source)
    elif Path(args.source).suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.jpeg']:
        monitor.monitor_image(args.source)
    else:
        print(f"❌ Error: Unknown source type: {args.source}")
        print("   Use 'webcam', video file (.mp4, .avi), or image file (.jpg, .png)")


if __name__ == "__main__":
    print("="*70)
    print("🦺 EDGE SAFETY MONITOR - Construction Site Safety Detection")
    print("="*70)
    main()