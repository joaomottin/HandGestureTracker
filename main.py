import cv2
from cvzone.HandTrackingModule import HandDetector

# Inicializa a webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Largura
cap.set(4, 720)   # Altura

# Inicializa o detector de mãos
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    # Captura frame da webcam
    success, img = cap.read()
    
    if not success:
        break
    
    # Detecta as mãos
    hands, img = detector.findHands(img)
    
    # Se detectar mãos, mostra informações
    if hands:
        for hand in hands:
            # Pega landmarks da mão
            lmList = hand["lmList"]  # Lista de 21 pontos da mão
            bbox = hand["bbox"]  # Bounding box
            handType = hand["type"]  # "Left" ou "Right"
            
            # Mostra tipo da mão
            cv2.putText(img, handType, (bbox[0], bbox[1] - 10),
                       cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    # Mostra o frame
    cv2.imshow("Hand Tracking", img)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
