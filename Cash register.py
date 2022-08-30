import pygame
# Color
Black = (0, 0, 0)
Light = (158, 158, 158)
Silver = (192, 192, 192)
Gray = (220, 220, 220)
Dark_Gray = (236, 236, 236)
Light_Blue = (204, 230, 252)
Dark_Blue = (0, 178, 191)
White = (255, 255, 255)

def draw(screen, font, text, color, x, y):
	text_render = font.render(text, True, color)			# Xác định cỡ chữ, chữ sẽ hiển thị và màu sắc
	screen.blit(text_render, (x, y))						# Hiển thị chữ lên màn hình ở vị trí tọa độ x, y cho trước

def input_box(screen, x, y, width, heigh):
	points = ((x - 5, y - 5), (x + width + 5, y - 5), (x + width, y), (x, y + heigh), (x - 5, y + heigh + 5))
	pygame.draw.rect(screen, White, (x - 5, y - 5, width + 10, heigh + 10))
	pygame.draw.polygon(screen, Gray, points) # Vẽ ra hình đa giác
	pygame.draw.rect(screen, Dark_Gray, (x, y, width, heigh))

def button_box(screen, x, y, width, heigh):
	points = ((x - 5, y + heigh + 5), (x, y + heigh), (x + width, y), (x + width + 5, y - 5), (x + width + 5, y + heigh + 5))
	pygame.draw.rect(screen, White, (x - 5, y - 5, width + 10, heigh + 10))
	pygame.draw.polygon(screen, Gray, points) # Vẽ ra hình đa giác
	pygame.draw.rect(screen, Dark_Gray, (x, y, width, heigh))

# Hàm lặp - mục đích: Tính từng mệnh giá trả lại khách hàng
def calc_return(change, List):								# Tiền thừa / trả lại: Change
	denominations = [100, 50, 20, 10, 5, 2, 1] 				# Mệnh giá: Denominations
	for money in denominations:
		if(change != None):
			change = return_cash(change, money, List)
	return List

def return_cash(change, money, List):
	if(change >= money):
		count = change / money
		if count >= 2:
			bill = "bills"
		else:
			bill = "bill"
		List.append("{0} ${1} {2}".format(str(int(count)), str(money), bill))
	else:
		return change									# Nếu sai thoát hàm return_cash luôn và return giá trị change ban đầu
	remaining_money = change % money 					# Số tiền còn lại: Remaining_money
	# Điều kiện kết thúc vòng lặp
	if(remaining_money != 0):
		if(remaining_money > 0 and remaining_money < 1):
			remaining_money	= remaining_money * 100
			if remaining_money >= 2:
				cent = "cents"
			else:
				cent = "cent"
			List.append('and ' + str(int(round(remaining_money,2))) + " " + cent)
		else:
			return remaining_money

def main():
	screen_x = 675
	screen_y = 600
	screen = pygame.display.set_mode((screen_x, screen_y))
	pygame.display.set_caption('Cash register')
	clock = pygame.time.Clock()

	# Font chữ
	font1 = pygame.font.SysFont('sans', 15)
	font2 = pygame.font.SysFont('sans', 20)
	font3 = pygame.font.SysFont('sans', 25)

	# Tọa độ
	x, y = [screen_x/9, screen_y/8]
	# Size button
	btn_x, btn_y = [5*screen_x/27, screen_y/12]
	# Khoảng cách thêm vào
	distance = 50
	add = 8

	# Xác định tọa độ 'Calculate':
	Text_calculate = font3.render('Calculate', True, Black)
	Text_C = Text_calculate.get_rect()
	text_C_x = Text_C[2]
	text_C_y = Text_C[3]

	# Xác định tọa độ 'Enough money !':
	Text_Infor = font3.render('Enough money !', True, Black)
	Text_I = Text_Infor.get_rect()
	text_I_x = Text_I[2]
	text_I_y = Text_I[3]

	# Xác định tọa độ 'Lack of money !':
	Text_Lack = font2.render('Lack of money !', True, Black)
	Text_L = Text_Lack.get_rect()
	text_L_x = Text_L[2]
	text_L_y = Text_L[3]

	user_text = ['', '', '']	# Weight, Price_Tag, Customer_money

	total = None
	weight = None
	active = None
	running = True
	price_tag = None
	customer_money = None

	while running:
		clock.tick(60)				# Dòng lệnh này sẽ nháy 60 lần/s		
		screen.fill(Light_Blue)		# Màu nền của chương trình
		pos_x, pos_y = pygame.mouse.get_pos()	# Lấy tọa độ chuột

		# Hiển thị nút bấm
		if active == 1:
			input_box(screen, x, y, btn_x, btn_y)
		else:
			button_box(screen, x, y, btn_x, btn_y)
		if active == 2:
			input_box(screen, 2*x + btn_x, y, btn_x, btn_y)
		else:
			button_box(screen, 2*x + btn_x, y, btn_x, btn_y)
		if active == 3:
			input_box(screen, 2*x + btn_x - 25, 2*y + btn_y, btn_x + 2*25, btn_y)
		else:
			button_box(screen, 2*x + btn_x - 25, 2*y + btn_y, btn_x + 2*25, btn_y)
		if active == 4 and total != None and customer_money != None:
			input_box(screen, 2*x + btn_x - 25, 2*y + 2*btn_y + distance, btn_x + 2*25, btn_y)
			pygame.draw.rect(screen, White, (x + btn_x, 2*y + 3*btn_y + 2*distance, 2*x + btn_x, 3*btn_y))
			if customer_money - total == 0:
				draw(screen, font3, 'Enough money !', Black, x + btn_x + (2*x + btn_x - 25 - text_I_x)/2, 2*y + 3*btn_y + 2*distance + (3*btn_y - text_I_y)/2)
			else:
				if customer_money - total < 0:
					lack = round(total - customer_money, 2)
					draw(screen, font3, "Lack of money !", Black, x + btn_x + (2*x + btn_x - 25 - text_L_x)/2, 2*y + 3*btn_y + 2*distance + (3*btn_y - text_L_y)/2)
					draw(screen, font2, str(lack) + " $", Black, x + btn_x + (2*x + btn_x - 25 - text_L_x)/2 + 30, 2*y + 3*btn_y + 2*distance + (3*btn_y - text_L_y)/2 + text_L_y + add)
				else:
					List = [] # List chứa thông tin tiền trả về
					Infor = calc_return(round(customer_money - total, 2), List)
					draw(screen, font2, "The amount to be returned:", Black, x + btn_x + add, 2*y + 3*btn_y + 2*distance + add)
					for i in range(len(List)):
						draw(screen, font2, List[i], Black, x + btn_x + add, 2*y + 3*btn_y + 2*distance + 2*add + text_L_y*(i+1))
		else:
			button_box(screen, 2*x + btn_x - 25, 2*y + 2*btn_y + distance, btn_x + 2*25, btn_y)
		input_box(screen, 3*x + 2*btn_x, y, btn_x, btn_y)

		# Hiển thỉ tiêu đề
		draw(screen, font2, 'Weight: (kg)', Black, x + add, y - add - text_L_y)
		draw(screen, font2, 'Price: ($/kg)', Black, 2*x + btn_x + add, y - add - text_L_y)
		draw(screen, font2, 'Total: ($)', Black, 3*x + 2*btn_x + add,y - add - text_L_y)
		draw(screen, font2, 'Customer money: ($)', Black, 2*x + btn_x - 25 + add, 2*y + btn_y - text_L_y - add)
		draw(screen, font3, 'Calculate', Black, 2*x + btn_x - 25 + (btn_x + 50 - text_C_x)/2, 2*y + 2*btn_y + distance + (btn_y - text_C_y)/2)

		# Hiển thị thông tin nhập từ bàn phím
		draw(screen, font2, user_text[0], Black, x + add, y + (btn_y - text_L_y)/2)
		draw(screen, font2, user_text[1], Black, 2*x + btn_x + add, y + (btn_y - text_L_y)/2)
		draw(screen, font2, user_text[2], Black, 2*x + btn_x - 25 + add, 2*y + btn_y + (btn_y - text_L_y)/2)
		if weight != None and price_tag != None:
			total = round(weight * price_tag, 2)
			if total != None:
				draw(screen, font2, str(total), Black, 3*x + 2*btn_x + add, y + (btn_y - text_L_y)/2)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (x < pos_x < x + btn_x and y < pos_y < y + btn_y):
						active = 1
					elif (2*x + btn_x < pos_x < 2*x + 2*btn_x and y < pos_y < y + btn_y):
						active = 2
					elif (2*x + btn_x - 25 < pos_x < 2*x + 3*btn_x + 25 and 2*y + btn_y < pos_y < 2*y + 2*btn_y):
						active = 3
					elif (2*x + btn_x - 25 < pos_x < 2*x + 3*btn_x + 25 and 2*y + 2*btn_y + distance < pos_y < 2*y + 3*btn_y + distance):
						active = 4
					else:
						active = None

			if event.type == pygame.KEYDOWN:
				for i in range(1, 4):
					if active == i:
						if event.key == pygame.K_RETURN:
							if i == 1:
								weight = float(user_text[i-1])
							if i == 2:
								price_tag = float(user_text[i-1])
							if i == 3:
								customer_money = float(user_text[i-1])
						elif event.key == pygame.K_BACKSPACE:
							user_text[i-1] = user_text[i-1][:-1]
						else:
							user_text[i-1] += event.unicode

		pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()
