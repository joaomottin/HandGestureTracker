import cv2
import math
from cvzone.HandTrackingModule import HandDetector

# Inicializa a webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Largura
cap.set(4, 720)   # Altura

# Inicializa o detector de mãos
detector = HandDetector(detectionCon=0.8, maxHands=2)

def calcular_distancia(ponto1, ponto2):
    """Calcula a distância euclidiana entre dois pontos"""
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

def identificar_forma(thumb1, index1, thumb2, index2):
    """
    Identifica a forma geométrica formada pelos 4 pontos dos dedos
    Analisa os ângulos e proporções reais do quadrilátero formado
    """
    
    # Os 4 pontos formam um quadrilátero
    # thumb1 (mão 1), index1 (mão 1), index2 (mão 2), thumb2 (mão 2)
    p1 = thumb1
    p2 = index1
    p3 = index2
    p4 = thumb2
    
    # Calcula os 4 lados do quadrilátero
    lado1 = calcular_distancia(p1, p2)  # thumb1 -> index1
    lado2 = calcular_distancia(p2, p3)  # index1 -> index2
    lado3 = calcular_distancia(p3, p4)  # index2 -> thumb2
    lado4 = calcular_distancia(p4, p1)  # thumb2 -> thumb1
    
    # Calcula as 2 diagonais
    diag1 = calcular_distancia(p1, p3)  # thumb1 -> index2
    diag2 = calcular_distancia(p2, p4)  # index1 -> thumb2
    
    # Calcula ângulos dos vértices usando produto escalar
    def calcular_angulo(p_anterior, p_centro, p_proximo):
        """Calcula o ângulo em graus no ponto p_centro"""
        v1 = (p_anterior[0] - p_centro[0], p_anterior[1] - p_centro[1])
        v2 = (p_proximo[0] - p_centro[0], p_proximo[1] - p_centro[1])
        
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # Limita entre -1 e 1
        angle = math.acos(cos_angle) * 180 / math.pi
        return angle
    
    # Calcula os 4 ângulos do quadrilátero
    ang1 = calcular_angulo(p4, p1, p2)
    ang2 = calcular_angulo(p1, p2, p3)
    ang3 = calcular_angulo(p2, p3, p4)
    ang4 = calcular_angulo(p3, p4, p1)
    
    # Calcula métricas para análise
    lados = [lado1, lado2, lado3, lado4]
    angulos = [ang1, ang2, ang3, ang4]
    
    lado_max = max(lados)
    lado_min = min(lados)
    lado_medio = sum(lados) / 4
    
    # Tolerância para comparação (em pixels)
    tolerancia = 0.20  # 20% de diferença é aceitável
    
    # Verifica similaridade entre lados
    def sao_similares(a, b, tol=tolerancia):
        return abs(a - b) / max(a, b) < tol if max(a, b) > 0 else True
    
    # Conta quantos ângulos são próximos de 90°
    angulos_90 = sum(1 for a in angulos if 75 < a < 105)
    angulos_agudos = sum(1 for a in angulos if a < 75)
    
    # Verifica se todos os lados são similares
    todos_lados_iguais = all(sao_similares(lado, lado_medio, 0.15) for lado in lados)
    
    # Verifica se lados opostos são similares
    lados_opostos_iguais = (sao_similares(lado1, lado3, 0.18) and sao_similares(lado2, lado4, 0.18))
    
    # Verifica se diagonais são similares
    diagonais_iguais = sao_similares(diag1, diag2, 0.15)
    
    # ============ DETECÇÃO DE FORMAS (ordem de prioridade) ============
    
    # 1. TRIÂNGULO: quando um lado é muito pequeno (quase colapsa)
    if lado_min < lado_max * 0.30:
        return "TRIANGULO", (255, 100, 0)
    
    # 1. TRIÂNGULO: quando um lado é muito pequeno (quase colapsa)
    if lado_min < lado_max * 0.30:
        return "TRIANGULO", (255, 100, 0)
    
    # 2. QUADRADO: todos os lados iguais + todos ângulos ~90° + diagonais iguais
    if todos_lados_iguais and angulos_90 >= 3 and diagonais_iguais:
        return "QUADRADO", (0, 255, 0)
    
    # 3. RETÂNGULO: lados opostos iguais + todos ângulos ~90° (diagonais iguais)
    if lados_opostos_iguais and angulos_90 >= 3:
        return "RETANGULO", (0, 200, 100)
    
    # 4. LOSANGO: todos os lados iguais + NÃO tem 4 ângulos retos
    if todos_lados_iguais and angulos_90 <= 2:
        return "LOSANGO", (0, 255, 255)
    
    # 5. PARALELOGRAMO: lados opostos iguais + ângulos NÃO são 90°
    if lados_opostos_iguais and angulos_90 <= 2:
        return "PARALELOGRAMO", (50, 150, 255)
    
    # 6. TRAPÉZIO: pelo menos um par de lados similares OU ângulos mistos
    if (sao_similares(lado1, lado3, 0.25) or sao_similares(lado2, lado4, 0.25)) and not todos_lados_iguais:
        return "TRAPEZIO", (100, 200, 255)
    
    # 7. Formas irregulares
    variacao_lados = (lado_max - lado_min) / lado_medio * 100 if lado_medio > 0 else 0
    
    # PENTÁGONO: variação moderada + mix de ângulos
    if 20 < variacao_lados < 55 and 1 <= angulos_90 <= 2:
        return "PENTAGONO", (200, 100, 255)
    
    # Padrão
    return "INDEFINIDO", (128, 128, 128)


while True:
    # Captura frame da webcam
    success, img = cap.read()
    
    if not success:
        break
    
    # Detecta as mãos
    hands, img = detector.findHands(img)
    
    # Se detectar 2 mãos, calcula distância
    if len(hands) == 2:
        # Pega landmarks de ambas as mãos
        hand1 = hands[0]
        hand2 = hands[1]
        
        lmList1 = hand1["lmList"]
        lmList2 = hand2["lmList"]
        
        # Landmark 8 = ponta do dedo indicador (index finger tip)
        # Landmark 4 = ponta do polegar (thumb tip)
        index1 = lmList1[8][:2]   # Ponta do indicador da mão 1
        thumb1 = lmList1[4][:2]   # Ponta do polegar da mão 1
        index2 = lmList2[8][:2]   # Ponta do indicador da mão 2
        thumb2 = lmList2[4][:2]   # Ponta do polegar da mão 2
        
        # Desenha linhas entre os pontos para visualizar
        # Linhas dos indicadores
        cv2.line(img, index1, index2, (0, 255, 0), 3)
        cv2.circle(img, index1, 8, (0, 255, 0), -1)
        cv2.circle(img, index2, 8, (0, 255, 0), -1)
        
        # Linhas dos polegares
        cv2.line(img, thumb1, thumb2, (255, 0, 0), 3)
        cv2.circle(img, thumb1, 8, (255, 0, 0), -1)
        cv2.circle(img, thumb2, 8, (255, 0, 0), -1)
        
        # Linhas conectando polegar-indicador (mesma mão)
        cv2.line(img, thumb1, index1, (100, 100, 100), 2)
        cv2.line(img, thumb2, index2, (100, 100, 100), 2)
        
        # Calcula distâncias
        distancia_index = calcular_distancia(index1, index2)
        distancia_thumb = calcular_distancia(thumb1, thumb2)
        
        # Identifica forma geométrica
        forma, cor = identificar_forma(thumb1, index1, thumb2, index2)
        
        # Mostra distâncias dos 4 lados do quadrilátero para debug
        lado1 = calcular_distancia(thumb1, index1)
        lado2 = calcular_distancia(index1, index2)
        lado3 = calcular_distancia(index2, thumb2)
        lado4 = calcular_distancia(thumb2, thumb1)
        
        cv2.putText(img, f"L1: {lado1:.0f} | L2: {lado2:.0f} | L3: {lado3:.0f} | L4: {lado4:.0f}", (50, 100),
                   cv2.FONT_HERSHEY_PLAIN, 1.3, (200, 200, 200), 1)
        
        # Mostra forma detectada (grande e destacado)
        cv2.putText(img, f"FORMA: {forma}", (300, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, cor, 3)
        
        # Mostra tipo de cada mão
        bbox1 = hand1["bbox"]
        bbox2 = hand2["bbox"]
        handType1 = hand1["type"]
        handType2 = hand2["type"]
        
        cv2.putText(img, handType1, (bbox1[0], bbox1[1] - 10),
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(img, handType2, (bbox2[0], bbox2[1] - 10),
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    elif len(hands) == 1:
        # Se só tem uma mão, mostra mensagem
        hand = hands[0]
        bbox = hand["bbox"]
        handType = hand["type"]
        
        cv2.putText(img, handType, (bbox[0], bbox[1] - 10),
                   cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, "Levante a outra mao", (50, 50),
                   cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    
    else:
        # Nenhuma mão detectada
        cv2.putText(img, "Coloque suas maos na frente da camera", (50, 50),
                   cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # Mostra o frame
    cv2.imshow("Hand Geometry Detector", img)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
