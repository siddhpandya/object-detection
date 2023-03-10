import numpy as np
import cv2
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable","dog", "horse", "motorbike", "person", "pottedplant", "sheep","sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("D:/MobileNet-SSD-master/deploy.prototxt","D:/MobileNet-SSD-master/mobilenet_iter_73000.caffemodel")
cap= cv2.VideoCapture(0)
while True:
	_,image = cap.read()
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,(300, 300), 127.5)
	print("[INFO] computing object detections...")
	net.setInput(blob)
	detections = net.forward()
	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence >= 0.1:
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
			print("[INFO] {}".format(label))
			cv2.rectangle(image, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(image, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	if cv2.waitKey(1) & 0xFF==ord('q'):
		break
	cv2.imshow("Output", image)