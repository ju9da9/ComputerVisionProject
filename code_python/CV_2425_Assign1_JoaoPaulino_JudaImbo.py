import os
import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math
import os
import csv
import sys

'''
Chamada das funções

'''
# Function to check if a point is within the circle's boundary
def is_point_in_circle(x, y, cx, cy, r):
    """
    Determines if a point is inside a given circle.

    Parameters:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        cx (float): The x-coordinate of the circle's center.
        cy (float): The y-coordinate of the circle's center.
        r (float): The radius of the circle.

    Returns:
        bool: True if the point (x, y) is inside the circle, False otherwise.
    """
    """Returns True if the point (x, y) is inside the circle with center (cx, cy) and radius r"""
    return (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2

#The agrupar_linhas function has the function of finding lines that are close together and nearly parallel to group into a group
'''
The angle_threshold variable is used to define the tolerance for grouping lines based on their orientation. It represents the maximum allowable difference in angle (in degrees) between two lines for them to be considered nearly parallel and eligible to be grouped together.

How It Works:
In this simplified version, each line’s angle is rounded to the nearest multiple of angle_threshold (e.g., 12 degrees). This rounding groups lines with similar angles into discrete “angle bins.” Lines that fall into the same bin (or near bins within the threshold) are considered parallel or almost parallel.

For example:

If angle_threshold = 12, the angles are rounded to multiples like 0°, 12°, 24°, etc.
Lines with actual angles of 11° and 15° would both round to 12°, allowing them to be grouped together.

Why It’s Useful:
This approach allows us to quickly check if two lines are parallel or nearly parallel without calculating exact angle differences each time. By setting angle_threshold to a value like 10-15 degrees, you allow a bit of flexibility, making the function more robust to slight variations in line angles.

Adjusting angle_threshold:
Higher values (e.g., 15° or 20°): Group lines more loosely, allowing for more angle variation.
Lower values (e.g., 5°): Make grouping stricter, requiring lines to be almost perfectly parallel to be grouped.
This threshold is useful in applications like clock hand detection, where the hour and minute hands might have slight deviations but should still be grouped together.




The proximity_threshold variable sets the maximum allowable distance between the centroids (midpoints) of two lines for them to be considered as part of the same group. It helps ensure that only lines that are not just parallel (or nearly parallel) but also close in space are grouped together.

How It Works
In this implementation, each line’s midpoint (centroid) is calculated. When determining if a line should be added to an existing group, the centroid of the line is compared to the centroid of that group. If the distance between them is less than proximity_threshold, the line is considered close enough to the group and is added.

Why It’s Useful:
The proximity_threshold ensures that only lines that are both:

    1.Close in space, and
    2.Have a similar angle

are grouped together. This spatial constraint prevents unrelated lines from being grouped due to mere angle similarity, which can improve the accuracy of the grouping.

Adjusting proximity_threshold:
Higher values (e.g., 30 or 40): Lines further apart will be grouped together, potentially capturing more distant but parallel lines.
Lower values (e.g., 10 or 15): Grouping will be stricter, requiring lines to be closer together.
For tasks like detecting clock hands, a reasonable proximity_threshold (e.g., 20 pixels) can help accurately group hands that are both close and parallel, while excluding nearby but unrelated lines.


'''
def agrupar_linhas (lines,pos_cir_x,pos_cir_y,raio,angle_threshold=12, proximity_threshold=20):
    
    """
    Agrupa linhas com base em ângulo e proximidade em relação a um círculo.
    Parâmetros:
    lines (list): Lista de linhas, onde cada linha é representada por uma lista de coordenadas [x1, y1, x2, y2].
    pos_cir_x (float): Coordenada x do centro do círculo.
    pos_cir_y (float): Coordenada y do centro do círculo.
    raio (float): Raio do círculo.
    angle_threshold (int, opcional): Limite de ângulo em graus para agrupar linhas. Padrão é 12.
    proximity_threshold (int, opcional): Limite de proximidade para agrupar linhas. Padrão é 20.
    Retorna:
    list: Lista de grupos, onde cada grupo é um dicionário com as chaves:
        'lines' (list): Lista de linhas pertencentes ao grupo.
        'angle' (float): Ângulo médio do grupo em graus.
        'centroid' (tuple): Centróide (ponto médio) do grupo.
    """
    
    grupos= []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        distancia1 = np.sqrt((x1 - pos_cir_x)**2 + (y1 - pos_cir_y)**2)
        distancia2 = np.sqrt((x2 - pos_cir_x)**2 + (y2 - pos_cir_y)**2)
        
        if((max(distancia1,distancia2) < raio) and (min(distancia1,distancia2) < raio*50/100)):
            # Calculate line angle in degrees and round to nearest multiple of angle_threshold
            angle = math.atan2(y2 - y1, x2 - x1)
            angle_deg = round(math.degrees(angle) / angle_threshold) * angle_threshold

            # Calculate line centroid (midpoint) for distance comparisons
            centroid = ((x1 + x2) / 2, (y1 + y2) / 2)

            # Check if line belongs to an existing group based on angle and proximity
            grouped = False
            for group in grupos:
                if abs(angle_deg - group['angle']) < angle_threshold:
                    # Check proximity to group’s centroid
                    group_centroid = group['centroid']
                    distance = np.sqrt((centroid[0] - group_centroid[0]) ** 2 + (centroid[1] - group_centroid[1]) ** 2)
                    if distance < proximity_threshold:
                        # Add line to group and update group centroid
                        group['lines'].append(line)
                        group['centroid'] = ((group_centroid[0] + centroid[0]) / 2, (group_centroid[1] + centroid[1]) / 2)
                        grouped = True
                        break

            if not grouped:
                grupos.append({'lines': [line], 'angle': angle_deg, 'centroid': centroid})

        else:
            centroid = ((x1 + x2) / 2, (y1 + y2) / 2)
            # Handle special case where condition is not met
            grupos.append({'lines': [line], 'angle': 0, 'centroid': centroid})

    return grupos
            


# The function distance between parallel lines has the function to calculate the distance between two parallel lines
def distance_between_parallel_lines(line1, line2):
    """
    Calculate the perpendicular distance between two parallel lines.
    Args:
        line1 (tuple): A tuple containing the coordinates of two points on the first line 
                       in the format ((x1_1, y1_1, x2_1, y2_1),).
        line2 (tuple): A tuple containing the coordinates of two points on the second line 
                       in the format ((x1_2, y1_2, x2_2, y2_2),).
    Returns:
        float: The perpendicular distance between the two parallel lines.
    """
    # Get the coordinates of two points on each line
    x1_1, y1_1, x2_1, y2_1 = line1[0]
    x1_2, y1_2, x2_2, y2_2 = line2[0]

    # Create two direction vectors of two straight lines
    vector1 = np.array([x2_1 - x1_1, y2_1 - y1_1])
    vector2 = np.array([x2_2 - x1_2, y2_2 - y1_2])

    #Creates a vector connecting a point on one line to a point on the other line
    vector_between_lines = np.array([x1_2 - x1_1, y1_2 - y1_1])

    #Calculates the perpendicular distance between the two lines.
    distance = np.abs(np.cross(vector1, vector_between_lines)) / np.linalg.norm(vector1)

    return distance


# The hands detection function has the function of finding the farthest endpoint from the clock center of a line segment among line segments
# in the same group to create a clock hand with the clock center point.
def detetar_ponteiros(grupos, pos_cir_x, pos_cir_y,ponteiro_segundos):
    
    """
    Detects the clock hands from groups of lines.
    Args:
        grupos (list): A list of dictionaries, where each dictionary contains a key 'lines' 
                        that maps to a list of lines. Each line is represented as a tuple of 
                        coordinates (x1, y1, x2, y2).
        pos_cir_x (float): The x-coordinate of the center of the clock.
        pos_cir_y (float): The y-coordinate of the center of the clock.
        ponteiro_segundos (bool): A flag indicating whether to consider the second hand.
    Returns:
        list: A list of tuples representing the detected clock hands. Each tuple contains:
                - The coordinates of the clock hand (x1, y1, x2, y2).
                - The maximum thickness of the clock hand.
                - The length of the clock hand.
    """
    # Initialize a list to store clock hands
    hands = []

    # Browse through groups of lines
    for group in grupos:
        # Get the list of lines in the group and number of lines
        lines = group['lines']
        num_lines = len(lines)

        # Initialize variables to store the maximum thickness and length of the lines
        max_thickness = 0
        max_length = 0
        
        # Browse lines in groups
        for i in range(num_lines):
            x1, y1, x2, y2 = lines[i][0]
            
            # Calculate the distance from two points to the center of the clock
            length1 = np.sqrt((x1 - pos_cir_x)**2 + (y1 - pos_cir_y)**2)
            length2 = np.sqrt((x2 - pos_cir_x)**2 + (y2 - pos_cir_y)**2)

            # Take the larger distance as the length of the line
            length = np.max([length1, length2])

            # If the length is greater than the current maximum length
            if length > max_length:
                max_length = length

                # Take the point farthest from the center as the end point of the clock hand
                if length == length1:
                    max_line = x1, y1, pos_cir_x, pos_cir_y
                else:
                    max_line = x2, y2, pos_cir_x, pos_cir_y

            # Browse through the remaining lines in the group
            for j in range(i+1, num_lines):
                # Calculate the distance between two lines using a distance_between_parallel_lines function
                thickness = distance_between_parallel_lines(lines[i], lines[j])

                # Update maximum thickness
                if (thickness > max_thickness):
                    max_thickness = thickness

        # Create a set of line, thickness and length
        line = max_line, max_thickness, max_length

        
        if ponteiro_segundos is False:
            # If the thickness is greater than 0, it means there are at least two parallel lines
            if max_thickness > 0:
                # Add this set to the clock hands list
                hands.append(line)
        else:   
            hands.append(line)
        
    # Sort the list of clock hands by length in descending order
    hands.sort(key=lambda x: x[2], reverse=True)

    # Take the first three clock hands as the clock hands
    hands = hands[:3]
        
    return hands


# The get_hands function has the function of accurately determining the hour, minute, and second hands
# from the 3 clock hands found in the hands_detection function.
def get_hands(hands):
    """
    Arrange and identify the clock hands (hour, minute, and second) based on their thickness and length.
    Parameters:
    hands (list): A list of tuples, where each tuple represents a clock hand with the following structure:
                  (hand_name, thickness, length)
    Returns:
    tuple: A tuple containing three elements:
           - hour_hand: The hand with the shortest length among the remaining hands after identifying the second hand.
           - minute_hand: The hand with the longest length among the remaining hands after identifying the second hand.
           - second_hand: The hand with the smallest thickness.
    """
    # Arrange the clock hands by thickness
    sorted_hands_by_thickness = sorted(hands, key=lambda hands: hands[1])
    
    if len(sorted_hands_by_thickness)==1:
        if len(sorted_hands_by_thickness[0][0])==4 and not isinstance (sorted_hands_by_thickness[0][1], list) and  not isinstance (sorted_hands_by_thickness[0][2], list):
            reorder_hands = [sorted_hands_by_thickness[0][0],sorted_hands_by_thickness[0][1],sorted_hands_by_thickness[0][2]]
            test1=True
            second_hand = reorder_hands
            hour_hand = reorder_hands
            minute_hand = reorder_hands
    else: 
        test1=False
        # The second hand is the hand with the smallest thickness
        second_hand = sorted_hands_by_thickness[0]

        # Remove the second hand from the list containing 3 clock hands
        hands.remove(second_hand)

        # Arrange the remaining 2 clock hands by length
        sorted_hands_by_length = sorted(hands, key=lambda hands: hands[2])

        
        # The hour hand is the hand with the shortest length and the remaining hand is the minute hand
        hour_hand = sorted_hands_by_length[0]
        
        #minute_hand = sorted_hands_by_length[1]

        if len(sorted_hands_by_length)==1:
            test2=True
            minute_hand = sorted_hands_by_length[0]
            # The hour hand is the hand with the shortest length and the remaining hand is the minute hand
            hour_hand = sorted_hands_by_length[0]
        else:
            test2=False
            hour_hand = sorted_hands_by_length[0]
            minute_hand = sorted_hands_by_length[1]
    
    

    return hour_hand, minute_hand, second_hand



# The get_hands function has the function of accurately determining the hour, minute, and second hands
# from the 3 clock hands found in the hands_detection function.
def get_hands_V(hands,second_hand):
    
    """
    Arrange the remaining 2 clock hands by length and determine the hour and minute hands.
    Parameters:
    hands (list): A list of clock hands, where each hand is represented by a tuple or list containing its properties.
    second_hand (optional): An optional parameter representing the second hand of the clock.
    Returns:
    tuple: A tuple containing the hour hand and the minute hand.
    """
    
    
    # Arrange the remaining 2 clock hands by length
    sorted_hands_by_length = sorted(hands, key=lambda hands: hands[2])

    if len(sorted_hands_by_length) == 1:
        test2 = True
        minute_hand = sorted_hands_by_length[0]
        # The hour hand is the hand with the shortest length and the remaining hand is the minute hand
        hour_hand = sorted_hands_by_length[0]
    else:
        if hands != []: 
            test2 = False
            hour_hand = sorted_hands_by_length[0]
            minute_hand = sorted_hands_by_length[1]
        else:
            if second_hand is not None:
                hour_hand = second_hand
                minute_hand = second_hand
        

    return hour_hand, minute_hand



# from the 3 clock hands found in the hands_detection function.
def get_hands_S(hands):
    """
    Identify and return the second hand from a list of clock hands.
    This function takes a list of clock hands, where each hand is represented
    as a tuple containing its properties. It sorts the hands by their length
    in descending order and returns the hand with the longest length, which
    is assumed to be the second hand.
    Args:
        hands (list of tuples): A list of tuples, where each tuple represents
                                a clock hand and contains its properties. The
                                third element of each tuple is the length of
                                the hand.
    Returns:
        tuple: The tuple representing the second hand, which is the hand with
               the longest length.
    """

    # Arrange the remaining 2 clock hands by length
    sorted_hands_by_length = sorted(hands, key=lambda hands: hands[2], reverse=True)

    # The hour hand is the hand with the shortest length and the remaining hand is the minute hand
    second_hand = sorted_hands_by_length[0]

    return second_hand




# Function to calculate coordinates of a rectangle surrounding a straight line
def calculate_rect_coordinates(line):
    """
    Calculate the coordinates and dimensions of a rectangle given a line.
    Args:
        line (list): A list containing a single tuple with four integers (x1, y1, x2, y2) 
                     representing the coordinates of two points on the line.
    Returns:
        tuple: A tuple containing six elements:
            - rect_x (int): The x coordinate of the top-left corner of the rectangle.
            - rect_y (int): The y coordinate of the top-left corner of the rectangle.
            - rect_width (int): The width of the rectangle.
            - rect_height (int): The height of the rectangle.
            - text_x (int): The x coordinate of the first point on the line.
            - text_y (int): The y coordinate of the first point on the line.
    """
    x1, y1, x2, y2 = line[0]

    # The x coordinate of the rectangle is the smallest value of x1 and x2
    # The y coordinate of the rectangle is the smallest value of y1 and y2
    rect_x = min(x1, x2)
    rect_y = min(y1, y2)

    # The width of the rectangle is the absolute value of the difference x2 and x1
    # The height of the rectangle is the absolute value of the difference y2 and y1
    rect_width = abs(x2 - x1)
    rect_height = abs(y2 - y1)

    # The coordinates of the location to note are the coordinates of the first point on the line
    text_x, text_y = x1, y1
    return rect_x, rect_y, rect_width, rect_height, text_x, text_y


#The draw_hands_frame function has the function of drawing a rectangular frame and labels for the clock hands
def draw_ponteiros_frame(img, hour_hand, minute_hand, second_hand):
    """
    Draws rectangles and labels for the hour, minute, and second hands on the given image.
    Parameters:
    img (numpy.ndarray): The image on which to draw the rectangles and labels.
    hour_hand (tuple): Coordinates and dimensions for the hour hand rectangle.
    minute_hand (tuple): Coordinates and dimensions for the minute hand rectangle.
    second_hand (tuple): Coordinates and dimensions for the second hand rectangle.
    Returns:
    None
    """
    # Draw rectangle and add label for hour hand
    rect_x, rect_y, rect_width, rect_height, text_x, text_y = calculate_rect_coordinates(hour_hand)
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 3)
    cv2.putText(img, 'Hour', (int(text_x), int(text_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Draw rectangle and add label for minute hand
    rect_x, rect_y, rect_width, rect_height, text_x, text_y = calculate_rect_coordinates(minute_hand)
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 3)
    cv2.putText(img, 'Minute', (int(text_x), int(text_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw rectangle and add label for second hand
    rect_x, rect_y, rect_width, rect_height, text_x, text_y = calculate_rect_coordinates(second_hand)
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (255, 0, 0), 3)
    cv2.putText(img, 'Second', (int(text_x), int(text_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


# Function to calculate direction vector of a clock hand
def get_vector(hand):
    """
    Calculate the vector from the coordinates of a hand.

    Args:
        hand (list): A list containing a single tuple with four integers (x1, y1, x2, y2) 
                     representing the coordinates of two points.

    Returns:
        list: A list containing two integers representing the vector [dx, dy] 
              where dx is the difference in x-coordinates and dy is the difference in y-coordinates.
    """
    x1, y1, x2, y2 = hand[0]
    vector = [x2 - x1, y2 - y1]
    return vector

# Function to calculate the dot product of two vectors
def dot_product(u, v):
    """
    Calculate the dot product of two 2-dimensional vectors.

    Args:
        u (list or tuple): A 2-dimensional vector represented as a list or tuple of two numbers.
        v (list or tuple): A 2-dimensional vector represented as a list or tuple of two numbers.

    Returns:
        float: The dot product of vectors u and v.

    Example:
        >>> dot_product([1, 2], [3, 4])
        11
    """
    return u[0] * v[0] + u[1] * v[1]

# The function calculates the directional product of two vectors
def cross_product(u, v):
    """
    Calculate the 2D cross product of two vectors.

    The cross product of two 2D vectors u and v is defined as:
    u[0] * v[1] - u[1] * v[0]

    Parameters:
    u (tuple or list): The first vector, represented as a tuple or list of two elements.
    v (tuple or list): The second vector, represented as a tuple or list of two elements.

    Returns:
    float: The scalar value of the 2D cross product.
    """
    return u[0] * v[1] - u[1] * v[0]


 #Function to calculate the angle of a clock hand relative to the y direction
def get_angle(hand, center_x, center_y):
    """
    Calculate the angle between the clock hand and the horizontal direction vector.
    Args:
        hand (list): The coordinates of the clock hand as a list [x, y].
        center_x (float): The x-coordinate of the center of the clock.
        center_y (float): The y-coordinate of the center of the clock.
    Returns:
        float: The angle in degrees between the clock hand and the horizontal direction vector.
    """
    # u is the direction vector of the clock hands
    u = get_vector(hand)

    # Create a horizontal direction vector from the center of the clock
    v = [center_x - center_x, center_y - (center_y-100)]

    # Call the function to calculate the dot product of two vectors
    dot_uv = dot_product(u, v)

    # Calculate the length of vector u and v
    length_u = math.sqrt(u[0]**2 + u[1]**2)
    length_v = math.sqrt(v[0]**2 + v[1]**2)

    # Calculate the cosine of the angle between two vectors using the formula u.v / (|u| * |v|)
    cos_theta = dot_uv / (length_u * length_v)

    # Limit the value of cos to the range [-1, 1] to avoid errors when calculating arccos
    cos_theta = max(min(cos_theta, 1.0), -1.0)

    # Calculate the angle using the formula arccos(cos_theta)
    theta = math.acos(cos_theta)

    # Convert angle from radians to degrees
    theta_degrees = math.degrees(theta)

    # If the directional product is greater than 0, that means vector u is to the left of vector v
    # Conversely, if the directional product is less than or equal to 0, that means vector u is to the right or in the same direction as vector v
    cross_uv = cross_product(u, v)
    if cross_uv > 0:
        # Returns the complementary angle of theta
        return 360 - theta_degrees
    else:
        return theta_degrees
    
# The get_time function has the function of calculating time from the angles of the clock hands
def get_time(hour_angle, minute_angle, second_angle):
    """
    Calculate the time in hh:mm:ss format from the angles of the hour, minute, and second hands.
    Args:
        hour_angle (float): The angle of the hour hand in degrees.
        minute_angle (float): The angle of the minute hand in degrees.
        second_angle (float): The angle of the second hand in degrees.
    Returns:
        str: The calculated time in hh:mm:ss format.
    """
        # Calculate the time from the angle of the hour hand by dividing by 30 (each hour corresponds to 30 degrees)
    hour = hour_angle / 30

    # Calculate minutes and seconds from the angle of the minute and second hands by dividing by 6 (each minute or second corresponds to 6 degrees)
    minute = minute_angle / 6
    second = second_angle / 6

    #Adjust to avoid errors

    # If the angle of the hour hand is close to an integer multiplied with 30 (i.e. close to a specific hour)
    # and the angle of the minute hand is close to 0 or 360 (i.e. close to 12 o'clock)
    if (round(hour)*30 - hour_angle <= 6) and ((355 < minute_angle and minute_angle < 360) or (minute_angle < 90)):
        # Round hour up or down
        hour = round(hour)
        if hour == 12:
            hour = 0
    
    # If the angle of the hour hand is close to a specific hour
    # and the angle of the minute hand is close to 360 (ie close to 12 o'clock)
    # Then set minute to 0
    if (hour_angle - hour*30 <= 6) and (355 < minute_angle and minute_angle < 360):
        minute = 0

    # If the angle of the minute hand is close to an integer multiplied with 6 (i.e. close to a specific minute)
    # and the angle of the second hand is approximately between 0 and 6 (i.e. 1 round of 60 seconds has passed).
    if (round(minute)*6 - minute_angle <= 6) and (second_angle < 6):
        # Round minutes up or down
        minute = round(minute)
        if minute == 60:
            minute = 0

    # If the angle of the minute hand is close to a specific minute
    # and the angle of the second hand is close to 360 (ie close to 12 o'clock)
    # Then set second to 0
    if (minute_angle - minute*30 <= 6) and (354 < second_angle and second_angle < 360):
        second = 0

    hour = int(hour)
    minute = int(minute)
    second = int(second)

    # Create a time series in hh:mm:ss format
    time = f"{hour:02d}:{minute:02d}:{second:02d}"\

    return time

# The draw_time function has the function of drawing time on a clock image
def draw_time(img, time):
    """
    Draws the given time as text on the provided image.
    Parameters:
    img (numpy.ndarray): The image on which to draw the time.
    time (str): The time string to be drawn on the image.
    Returns:
    None
    """
    # Choose the font, size and thickness of the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 3

    # Choose a location to write text on the image
    text_position = (120, 120)

    # Choose the color of the text
    text_color = (0, 0, 255)

    # Write text on the image with selected parameters
    cv2.putText(img, time, text_position, font, font_scale, text_color, font_thickness)
    
def detect_region_of_interest(detect_circles,image,gray_mode,video_mode):
    
    """
    Detects the region of interest (ROI) in an image by identifying the largest circle using the HoughCircles method.
    Parameters:
    detect_circles (numpy.ndarray): Array of detected circles, where each circle is represented by its center coordinates (x, y) and radius.
    image (numpy.ndarray): The input image in which circles are to be detected.
    gray_mode (bool): Flag indicating if the image is in grayscale mode.
    video_mode (bool): Flag indicating if the function is being used in video mode. If False, the function will display the images.
    Returns:
    tuple: A tuple containing:
        - masked_image (numpy.ndarray): The image with the detected circle masked.
        - pos_cir_x (int): The x-coordinate of the center of the largest detected circle.
        - pos_cir_y (int): The y-coordinate of the center of the largest detected circle.
        - raio_cir (int): The radius of the largest detected circle.
    """
    #Código para detetar círculos baseado no link:
    #https://docs.opencv.org/4.x/d3/de5/tutorial_js_houghcircles.html

    '''
    Código para criar um contorno da região do relógio analógico with HoughCircles
    parametros:

    gray_image: nome da imagem,
    method = cv2.HOUGH_GRADIENT_ALT - método usado para a deteção de círculos, mas usado para garantir uma maior precisão
    dp =1 --> inverse ratio of the accumulator resolution to the image resolution. f dp = 1 , the accumulator has the same resolution as the input image
    minDist =20 --> minimum distance between the centers of the detected circles
    param1 --> referente ao gradiente Canny
    param2 -->


    '''
    'No caso de existir círculos:'
    if detect_circles is not None:
        
        detect_circles = np.around(detect_circles)
        
        maior_circulo = None
        centro_circulo = 0
        raio_maximo = 0
        
        #Nota: a variável detect_circles contêm três conteúdos a serem guardados: posição 0 --> x, posição 1 --> y, -->(posições do centro do círculo), posição 2 --> raio
        for i in detect_circles[0, :]:
            if i[2] > raio_maximo:
                raio_maximo = i[2] #atualiza o valor do raio máximo
                maior_circulo = i  # vai guardar as posições do círculo e o raio: posição 0 --> x, posição 1 --> y, -->(posições do centro do círculo), posição 2 --> raio
        
        
        if maior_circulo is not None:
            
                #Afunção cv2.circle apenas recebe os parâmetros do centro e do raio com tipo 'int', como a função cv2.circle 
                #precisa de valores da posição do centro do círculo e do raio a inteiro
                pos_cir_x = int(maior_circulo[0])
                pos_cir_y = int(maior_circulo[1])
                raio_cir = int(maior_circulo[2])
            
                # Dsenha o maior círculo e define a região de interesse à volta da área de relógio (denominado de mask)
                mask = np.zeros_like(image)
                
                # Draw a filled white circle on the mask
                cv2.circle(mask, (pos_cir_x, pos_cir_y), raio_cir, (255, 255, 255), thickness=-1)
                
                # Apply the mask to the original grayscale image using bitwise AND
                masked_image = cv2.bitwise_and(image, image, mask=mask)
 
                if video_mode is False:
                    # Mostar o resultado das imagens
                    cv2.imshow('Original Image with Detected Circle', image)
                    cv2.imshow('Clock Face Mask', mask)   
                    cv2.imshow('Masked Clock Face', masked_image) 
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    
                    
                    print(f"Maior círculo: centro do círculo = ({maior_circulo[0]}, {maior_circulo[1]}), radius = {maior_circulo[2]}")
                
        else:
            print("No circles were found." )     
            
    return masked_image, pos_cir_x, pos_cir_y, raio_cir    

def detect_ponteiros(image,S_image,V_image,masked_image,pos_cir_x, pos_cir_y, raio_cir,gray_mode,video_mode):
    
    """
    Detects the clock hands (hour, minute, and second hands) from an image of a clock.
    Parameters:
    image (numpy.ndarray): The original image of the clock.
    S_image (numpy.ndarray): The S channel of the HSV image.
    V_image (numpy.ndarray): The V channel of the HSV image.
    masked_image (numpy.ndarray): The masked image used for detection.
    pos_cir_x (int): The x-coordinate of the center of the clock.
    pos_cir_y (int): The y-coordinate of the center of the clock.
    raio_cir (int): The radius of the clock.
    gray_mode (bool): If True, the image is processed in grayscale mode.
    video_mode (bool): If True, the function is used in video mode.
    Returns:
    numpy.ndarray: The image with detected clock hands and time drawn on it.
    tuple: (Optional) The detected time if video_mode is True.
    Notes:
    This function is adapted from the work available at: 
    https://github.com/trietcs/clock-time-extraction-opencv
    """
    '''
    Deteção das linhas.

    Adaptado do trabalho realizado deste link: https://github.com/trietcs/clock-time-extraction-opencv

    '''    
    
    if gray_mode is True:
        
        #As variáveis S_image e V_image estão declaradas a 'None' visto que não são usadas quando gray_mode=TRUE
        S_image = None
        V_image = None
        
        #METODO NOVO
        _, thresh = cv2.threshold(masked_image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        cv2.imshow('Threshold - Gray', thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Blur the image with a Gaussian filter to reduce noise
        blurred = cv2.GaussianBlur(thresh, (5, 5), 0)
        
        cv2.imshow('Blur Applied - Gray', blurred)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #O USO DO BLURRED IMAGE NÃO ERA SUFICIENTE PORQUE AINDA EXISTIA ALGUMAS IMAGENS QUE NÃO PASSAVAM NO CENTRO DA IMAGEM 
        #Por Isso foi usado o canny para filtrar ae encontrar linhas na imagem
        # Use Canny filter to find edges in image
        edges = cv2.Canny(blurred, 50, 150)
        
        cv2.imshow('Edges by canny - Gray', edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        
        # Step 8: Use Hough Line Transformation to detect lines (clock hands)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=85, minLineLength=30, maxLineGap=5)
        
        
        # Step 9: Draw the lines that are within the circle
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Extract the line coordinates
                
                # Only draw the line if both endpoints are inside the circle
                new_line=cv2.line(masked_image, (x1, y1), (x2, y2), (255,255, 0), 2)
        
        if video_mode is False:
            cv2.imshow('Lines within Circle ', new_line)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Step 4: finding lines that are close together and nearly parallel to group into a group
        grupos = agrupar_linhas(lines, pos_cir_x, pos_cir_y, raio_cir)
        
        # Step 5: detect the clock hands
        ponteiros = detetar_ponteiros(grupos, pos_cir_x, pos_cir_y,ponteiro_segundos=False)
        
        # Step 6: Determine which hand is the hour hand, which hand is the minute hand, and which hand is the second hand
        hour_hand, minute_hand, second_hand = get_hands(ponteiros)
        
    else:
        
        
        circle_mask_S = np.zeros(S_image.shape[:2], dtype=np.uint8)
        
        cv2.circle(circle_mask_S,(pos_cir_x, pos_cir_y), raio_cir, 255, thickness=-1)

        # Step 6: Apply the mask to the cropped region
        S_image_cropped = cv2.bitwise_and(S_image, S_image, mask=circle_mask_S)
        
        if video_mode is False:
            cv2.imshow('Clock Face Mask - S_image',circle_mask_S)
            cv2.imshow('Masked Clock Face - S_image', S_image_cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        
        circle_mask_V = np.zeros(V_image.shape[:2], dtype=np.uint8)
        
        cv2.circle(circle_mask_V,(pos_cir_x, pos_cir_y), raio_cir, 255, thickness=-1)

        # Step 6: Apply the mask to the cropped region
        V_image_cropped = cv2.bitwise_and(V_image, V_image, mask=circle_mask_S)
        if video_mode is False:
            cv2.imshow('Clock Face Mask - V_image',circle_mask_V)
            cv2.imshow('Masked Clock Face - V_image', V_image_cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        
        
        #MODIFICAR ISTO 
        _, thresh_S = cv2.threshold(S_image_cropped, 127, 255, cv2.THRESH_BINARY)
        _, thresh_V = cv2.threshold(V_image_cropped, 127, 255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)

        
        if video_mode is False:
            cv2.imshow('Masked Clock Face - threshold - S', thresh_S)
            cv2.imshow('Masked Clock Face - threshold - V', thresh_V)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            

        
        # Blur the image with a Gaussian filter to reduce noise
        blurred_S = cv2.GaussianBlur(thresh_S, (5, 5), 0)

        
        # Blur the image with a Gaussian filter to reduce noise
        blurred_V = cv2.GaussianBlur(thresh_V, (5, 5), 0)

        
        if video_mode is False:

            cv2.imshow('Masked Clock Face - blurred S ', blurred_S)
            cv2.imshow('Masked Clock Face - blurred V ', blurred_V)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        #O USO DO BLURRED IMAGE NÃO ERA SUFICIENTE PORQUE AINDA EXISTIA ALGUMAS IMAGENS QUE NÃO PASSAVAM NO CENTRO DA IMAGEM 
        #Por Isso foi usado o canny para filtrar ae encontrar linhas na imagem
        # Use Canny filter to find edges in image
        edges_S = cv2.Canny(blurred_S, 50, 180) #150
        
        edges_V = cv2.Canny(blurred_V, 50, 195) #150

        if video_mode is False:
            # Step 10: Show the result
            cv2.imshow('edges_S', edges_S)            
            cv2.imshow('edges_V', edges_V)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        
        # Step 8: Use Hough Line Transformation to detect lines (clock hands)
        lines_S = cv2.HoughLinesP(edges_S, 1, np.pi / 180, threshold=85, minLineLength=30, maxLineGap=5)
        
        lines_V = cv2.HoughLinesP(edges_V, 1, np.pi / 180, threshold=85, minLineLength=30, maxLineGap=5)

        # Step 9: Draw the lines that are within the circle
        if lines_S is not None:
            for line_S in lines_S:
                x1, y1, x2, y2 = line_S[0]  # Extract the line coordinates
                
                # Only draw the line if both endpoints are inside the circle
                new_line_S=cv2.line(circle_mask_S, (x1, y1), (x2, y2), (0,255, 0), 2)   #masked_image   
                
        if lines_V is not None:
            for line_V in lines_V:
                x1, y1, x2, y2 = line_V[0]  # Extract the line coordinates
                
                # Only draw the line if both endpoints are inside the circle
                new_line_V=cv2.line(circle_mask_V , (x1, y1), (x2, y2), (0,255, 0), 2)   #masked_image     
            
        if video_mode is False:
            # Step 10: Show the result
            cv2.imshow('Lines within Circle S', new_line_S)    
            cv2.imshow('Lines within Circle V', new_line_V)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Step 4: finding lines that are close together and nearly parallel to group into a group
        grupos_S = agrupar_linhas(lines_S, pos_cir_x, pos_cir_y, raio_cir)
        
        # Step 4: finding lines that are close together and nearly parallel to group into a group
        grupos_V = agrupar_linhas(lines_V, pos_cir_x, pos_cir_y, raio_cir)
        
        # Step 5: detect the clock hands
        ponteiros_S = detetar_ponteiros(grupos_S, pos_cir_x, pos_cir_y,ponteiro_segundos=True)
        
        # Step 5: detect the clock hands
        ponteiros_V = detetar_ponteiros(grupos_V, pos_cir_x, pos_cir_y,ponteiro_segundos=False)

        second_hand = get_hands_S(ponteiros_S)
        
        hour_hand, minute_hand = get_hands_V(ponteiros_V,second_hand)



    # Step 7: draw a frame around and label the clock hands back on the image
    draw_ponteiros_frame(image, hour_hand, minute_hand, second_hand)

    # Step 8: determine the rotation angle of the clock hands
    hour_angle = get_angle(hour_hand, pos_cir_x,pos_cir_y)
    minute_angle = get_angle(minute_hand, pos_cir_x, pos_cir_y)
    second_angle = get_angle(second_hand, pos_cir_x, pos_cir_y)

    # Step 9: calculate the clock time based on the rotation angle in step 8
    time = get_time(hour_angle, minute_angle, second_angle)

    # Step 10: draw time on the image
    draw_time(image, time)
    

    if video_mode is False:
        output_dir = r'C:\Users\judai\Desktop\Trabalhos praticos - python\Trabalho_pratico_1\code_python\Trabalho exemplo\clock-time-extraction-opencv-main'
        filename = r'C:\Users\judai\Desktop\Trabalhos praticos - python\Trabalho_pratico_1\code_python'

        result_path = os.path.join(output_dir, f"result_{filename}.jpg")
        cv2.imwrite(result_path, image)
        return image
    else:
        return image, time

def main():
    """
    Main function to analyze clock images or videos and detect clock hands.
    This function allows the user to choose between analyzing an image or a video and whether to use grayscale or HSV color space for the analysis. 
    It performs the following tasks based on the selected modes:
    - Reads and verifies the input image or video.
    - Converts the image to grayscale or HSV color space.
    - Detects circles in the image to identify the clock face.
    - Masks the region of interest (clock face) for further analysis.
    - Detects clock hands within the masked region.
    - Displays the processed images and results.
    - Writes the detected time to a CSV file if video mode is selected.
    Variables:
    - gray_mode (bool): Determines if the image is analyzed in grayscale ('True') or HSV color space ('False').
    - video_mode (bool): Determines if the analysis is performed on a video ('True') or an image ('False').
    Note:
    - Video mode is only available in HSV color space. If both gray_mode and video_mode are set to True, the program will exit with an error message.
    """
    
    '''
    
    Variavel que determina se a imagem a ser analisada estara em escalade cizas ('True') ou em escala de cores HSV ('False')
    
    '''
    gray_mode = False
    
    '''
    
    Variável que determina se pretende-se realizar a detecao de ponteiros de uma imagem ou num video
    
    '''
    video_mode = False
    
    #Condição para impedir que corra o modo video em HSV. 
    #O modo video só se encontra disponível em escala de cinzas (gray_mode=True)
    if gray_mode is True and video_mode is True:
        print('\n\nO modo video só se encontra disponível na escala de cores HSV. Mude gray_mode a False caso queira ver o video na de cores HSV OU mude video_mode para False se deseja ver a deteção dos ponteiros de relógio por imagens em escala de cinzas\n\n ')
        sys.exit()
        
    else:
    
        if gray_mode is True:
            
            
                
                ''' 
                Leitura da imagem e verificação da mesma
                '''
                img = cv2.imread(r'../data/clock.png',cv2.IMREAD_COLOR)

                assert img is not None, "file could not be read, check with os.path.exists()"
                            
                '''
                Converter a imagem para a escala de cinzas
                '''
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
                
                cv2.imshow('Grayscale Image',gray_image)
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                
                detect_circles_gray = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=50, minRadius=180, maxRadius=197)

                #função para detetar a região de interesse com a grayscale
                masked_image_GRAY, pos_cir_x_GRAY, pos_cir_y_GRAY, raio_cir_GRAY = detect_region_of_interest(detect_circles_gray,gray_image,gray_mode,video_mode)

                cv2.imshow('Masked Clock Face - GRAYSCALE', masked_image_GRAY)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                #função para detetar os ponteiros dentro da regiao de interesse com a grayscale
                #NOTA: A declaração desta função está com o nome da variável usada dentro da função com o propósito de 
                # não mencionar as variáveis S_image e V_image que não são usadas com  gray_mode = TRUE
                horas_GRAY = detect_ponteiros(image=img,S_image=None,V_image=None, masked_image=masked_image_GRAY,pos_cir_x=pos_cir_x_GRAY, pos_cir_y=pos_cir_y_GRAY, raio_cir=raio_cir_GRAY,gray_mode=gray_mode,video_mode=video_mode)
                
                cv2.imshow('HORAS - GRAYSCALE', horas_GRAY)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
        else:
            
            if video_mode is True:
                cap = cv2.VideoCapture(r'../data/clock.mp4')
                while not cap.isOpened():
                    cap = cv2.VideoCapture(r'../data/clock.mp4')
                    
                csv_output_path = "clock_time.csv"    
                cv2.waitKey(1000)
                print("Wait for the header")
                pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

                
                #PARÂMETROS A SEREM AJUSTADOS
                
                
                # Set the starting frame (e.g., frame 100)
                starting_frame = 0
                # Set delay in milliseconds (1000ms = 1 second)
                delay = 10  # Adjust delay for slower playback (200ms = 0.2 seconds per frame)                

                # Set the starting frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)
                print(f"Starting processing from frame {starting_frame}.")
                
                # Prepare CSV file
                with open(csv_output_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Write header with student group details
                    writer.writerow(["#Group 6", "2230075", "João Paulino", "2232626", "Judá Imbó"])


                    print("Processing video...")
                    
                    while True:
                        flag, frame = cap.read()
                        if flag:
                            # The frame is ready and already captured
                        
                            '''
                            Converter a imagem para a escala de cores HSV
                            '''
                            HSV_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                            H_image, S_image, V_image = cv2.split(HSV_image)
                            pos_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                            
                    
                            detect_circles_HSV = cv2.HoughCircles(V_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=50, minRadius=180, maxRadius=197)

                            #função para detetar a região de interesse 
                            masked_image_HSV, pos_cir_x_HSV, pos_cir_y_HSV, raio_cir_HSV = detect_region_of_interest(detect_circles_HSV,V_image,gray_mode,video_mode)
                            
                            horas_HSV, time = detect_ponteiros(frame,S_image,V_image,masked_image_HSV,pos_cir_x_HSV, pos_cir_y_HSV, raio_cir_HSV,gray_mode,video_mode)
                            

                            print(f"Frame {pos_frame}: {time}")
                            
                            # Write to CSV
                            writer.writerow(["Frame "+str(pos_frame), time])

                            
                            cv2.imshow('video', horas_HSV)
                            # Wait for the specified delay, press 'q' to exit
                            if cv2.waitKey(delay) & 0xFF == ord('q'):
                                break
                            
                            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                                # If the number of captured frames is equal to the total number of frames,
                                # we stop
                                break
                            
            
                # Release resources
                cap.release()
                cv2.destroyAllWindows()
                
            else:
            
            
                
                ''' 
                Leitura da imagem e verificação da mesma
                '''
                img = cv2.imread(r'../data/clock.png',cv2.IMREAD_COLOR)

                assert img is not None, "file could not be read, check with os.path.exists()"            
                
                
                '''
                Converter a imagem para a escala de cores HSV
                '''
                HSV_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                H_image, S_image, V_image = cv2.split(HSV_image)
                
                
                
                cv2.imshow('HSV scale Image',HSV_image)
                cv2.imshow('H scale Image',H_image)
                cv2.imshow('S scale Image',S_image)
                cv2.imshow('V scale Image',V_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


                detect_circles_HSV = cv2.HoughCircles(V_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=50, minRadius=180, maxRadius=197)

                #função para detetar a região de interesse 
                masked_image_HSV, pos_cir_x_HSV, pos_cir_y_HSV, raio_cir_HSV = detect_region_of_interest(detect_circles_HSV,V_image,gray_mode,video_mode)

                cv2.imshow('Masked Clock Face - HSV', masked_image_HSV)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                horas_HSV = detect_ponteiros(img,S_image,V_image,masked_image_HSV,pos_cir_x_HSV, pos_cir_y_HSV, raio_cir_HSV,gray_mode,video_mode)
                
                cv2.imshow('HORAS - HSV', horas_HSV)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

