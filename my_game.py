import pygame
import random
import db_config

# DB
db_cf = db_config.DbConfig()
db = db_cf.client.dbmygame

# 현재 로그인 한 유저의 ID
current_user_id = ''
# 현재 로그인한 유저의 랭킹
current_user_ranking = 0
total_user = 0
# 현재 로그인 한 유저의 총 강화 횟수
current_count_ug = 0

# 게임 엔진 초기화
pygame.init()

# Input Text 색상/폰트
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont("malgungothic", 22)

# RGB 색상 세팅
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE_YELLOW = (255, 255, 102)

# 화면 크기 세팅
size = [334, 289]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("스타포스 강화")

# 사운드
clickSound = pygame.mixer.Sound("static/sound/click.wav")
clickSound.set_volume(0.3)
successSound = pygame.mixer.Sound("static/sound/ug_success.wav")
progressingSound = pygame.mixer.Sound("static/sound/ug_progress.wav")
catchSound = pygame.mixer.Sound("static/sound/catch_success.wav")

# 이미지
login = pygame.image.load("static/img/login.png")
hint = pygame.image.load("static/img/hint.png")
frame = pygame.image.load("static/img/frame.png")
confirm = pygame.image.load("static/img/confirm_upgrade.png")
upgrade = pygame.image.load("static/img/star_upgrade.png")
star = pygame.image.load("static/img/star.png")
upgrade_success = pygame.image.load("static/img/upgrade_success.png")
upgrade_fail = pygame.image.load("static/img/upgrade_fail.png")
upgrade_down = pygame.image.load("static/img/upgrade_down.png")
upgrade_destroy = pygame.image.load("static/img/upgrade_destroy.png")

# 종료 조건 세팅
done = False
clock = pygame.time.Clock()

# 상태 Flag
isLoginActivated = True
isHomeActivated = False
isCfActivated = False
isUgActivated = False
isNoStarCatch = False
isSuccessCatch = False
isUgResultActivated = False
isIdInputActivated = True
isFailToLogin = False
isHintActivated = False

# 인게임 전역 변수
current_ug = 0
starX = 149
starY = 191
starDirection = 1
starSpeed = 1.5 + (1.1 * current_ug)
upgradeResult = ''

# 강화 확률
general_percentages = {
    'star_1': [95, 5, 0, 0],
    'star_2': [90, 10, 0, 0],
    'star_3': [85, 15, 0, 0],
    'star_4': [80, 20, 0, 0],
    'star_5': [75, 15, 10, 0],
    'star_6': [70, 10, 20, 0],
    'star_7': [65, 0, 35, 0],
    'star_8': [60, 0, 40, 0],
    'star_9': [55, 0, 45, 0],
    'star_10': [50, 0, 50, 0],
    'star_11': [45, 0, 55, 0],
    'star_12': [35, 0, 65, 0],
    'star_13': [30, 0, 65, 5],
    'star_14': [30, 0, 64, 6],
    'star_15': [30, 0, 63, 7],
    'star_16': [30, 0, 62, 8],
    'star_17': [30, 0, 61, 9],
    'star_18': [30, 0, 60, 10],
    'star_19': [30, 0, 59, 11],
    'star_20': [30, 0, 58, 12],
    'star_21': [30, 0, 57, 13],
    'star_22': [30, 0, 56, 14],
    'star_23': [30, 0, 55, 15],
    'star_24': [30, 0, 54, 16],
    'star_25': [30, 0, 53, 17],
    'star_26': [30, 0, 52, 18],
    'star_27': [30, 0, 51, 19],
    'star_28': [30, 0, 50, 20],
    'star_29': [30, 0, 50, 20],
    'star_30': [30, 0, 50, 20]
}

plus_percentages = {
    'star_1': [95, 5, 0, 0],
    'star_2': [95, 5, 0, 0],
    'star_3': [90, 10, 0, 0],
    'star_4': [85, 15, 0, 0],
    'star_5': [80, 10, 10, 0],
    'star_6': [75, 5, 20, 0],
    'star_7': [70, 0, 30, 0],
    'star_8': [65, 0, 35, 0],
    'star_9': [60, 0, 40, 0],
    'star_10': [54, 0, 46, 0],
    'star_11': [49, 0, 51, 0],
    'star_12': [39, 0, 61, 0],
    'star_13': [34, 0, 61, 5],
    'star_14': [34, 0, 60, 6],
    'star_15': [34, 0, 59, 7],
    'star_16': [33, 0, 59, 8],
    'star_17': [33, 0, 58, 9],
    'star_18': [33, 0, 57, 10],
    'star_19': [33, 0, 56, 11],
    'star_20': [33, 0, 55, 12],
    'star_21': [32, 0, 55, 13],
    'star_22': [32, 0, 54, 14],
    'star_23': [32, 0, 53, 15],
    'star_24': [32, 0, 52, 16],
    'star_25': [32, 0, 51, 17],
    'star_26': [32, 0, 50, 18],
    'star_27': [32, 0, 49, 19],
    'star_28': [32, 0, 48, 20],
    'star_29': [32, 0, 48, 20],
    'star_30': [32, 0, 48, 20]
}


# 랭킹갱신
def refreshRank():
    global total_user, current_user_ranking, current_ug
    total_user = db.user.count_documents({})
    current_user_ranking = db.user.count_documents({'current_ug': {"$gt": current_ug}}) + 1
    total = db.user.find({}).count()

# 로그인
def doLogin(user_id, user_pw):
    user_id = user_id.strip()
    user_pw = user_pw.strip()
    global current_user_id, current_count_ug, current_ug, current_user_ranking, total_user
    user = db.user.find_one({'user_id': user_id})

    # DB에 존재하는 ID와 PW를 입력 / 로그인 성공
    if user is not None:
        if user['user_pw'] == user_pw:
            total_user = db.user.count_documents({})
            current_user_id = user_id
            current_count_ug = int(user['count_ug'])
            current_ug = int(user['current_ug'])
            current_user_ranking = db.user.count_documents({'current_ug': {"$gt": current_ug}}) + 1

            print("로그인 성공")
            print("전체 유저 : ", total_user)
            print("랭킹 : ", current_user_ranking)
            return True

        # 로그인 실패 : 패스워드 불일치
        else:
            print("로그인 실패")
            return False

    # DB에 존재하지 않는 ID와 PW를 입력 / 회원가입
    else:
        doc = {'user_id': user_id, 'user_pw': user_pw, 'current_ug': 0, 'count_ug': 0}
        db.user.insert_one(doc)
        current_user_id = user_id
        current_count_ug = 0
        current_ug = 0
        print("회원가입 성공")
        return True


# 저장
def saveStatus():
    # 현재 상태(총 강화 횟수, 현재 강화 수치) UPDATE
    db.user.update_one({'user_id': current_user_id}, {'$set': {'count_ug': current_count_ug, 'current_ug': current_ug}})


# Text Input 클래스
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode != '\t':
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        # pygame.draw.rect(screen, self.color, self.rect, 2)


# 강화 메인 로직
def calculation(percentages):
    global current_ug, current_count_ug
    # 1~100까지 중복 없는 난수로 채워져 있는 aList 생성
    if current_ug < 30:
        alist = []
        for i in range(1, 101):
            a = random.randint(1, 100)
            while a in alist:
                a = random.randint(1, 100)
            alist.append(a)

        success_list = []
        keep_list = []
        down_list = []
        destroy_list = []
        success = percentages['star_' + str(current_ug + 1)][0]
        keep = percentages['star_' + str(current_ug + 1)][1]
        down = percentages['star_' + str(current_ug + 1)][2]
        destroy = percentages['star_' + str(current_ug + 1)][3]

        for i in range(0, success):
            success_list.append(alist[i])

        for i in range(success, success + keep):
            keep_list.append(alist[i])

        for i in range(success + keep, success + keep + down):
            down_list.append(alist[i])

        for i in range(success + keep + down, success + keep + down + destroy):
            destroy_list.append(alist[i])

        user_number = random.randint(1, 100)

        if user_number in success_list:
            current_count_ug += 1
            current_ug += 1
            saveStatus()
            refreshRank()
            return 'success'
        elif user_number in keep_list:
            current_count_ug += 1
            current_ug += 0
            saveStatus()
            refreshRank()
            return 'keep'
        elif user_number in down_list:
            current_count_ug += 1
            current_ug -= 1
            saveStatus()
            refreshRank()
            return 'down'
        elif user_number in destroy_list:
            current_count_ug += 1
            current_ug = 0
            saveStatus()
            refreshRank()
            return 'destroy'

    return 'keep'


# 강화 시작
def startUpgrade():
    print("현재 강화 : ", current_ug)

    # 스타캐치 해제
    if isNoStarCatch:
        print('스타캐치 해제 강화')
        progressingSound.play()
        pygame.time.wait(1000)
        progressingSound.play()
        pygame.time.wait(1000)
        print("강화 완료")
        return calculation(general_percentages)

    # 스타캐치 설정
    else:
        print("현재 강화 : ", current_ug)
        print('스타캐치 설정 강화')

        # 스타캐치 성공/실패 메세지
        if isSuccessCatch:
            createText("★CATCH★", 40, 65, 105, WHITE_YELLOW)
            pygame.display.update()
        else:
            createText("MISS", 50, 105, 115, RED)
            pygame.display.update()

        # 스타캐치 성공 시 사운드 재생
        pygame.time.wait(700)
        progressingSound.play()
        pygame.time.wait(1000)
        progressingSound.play()
        pygame.time.wait(1000)
        if isSuccessCatch:
            print("확률 증가 후 강화 완료")
            return calculation(plus_percentages)
        else:
            print("확률 증가 없이 강화 완료")
            return calculation(general_percentages)


# 텍스트 그리기
def createText(text, font_size, x, y, color):
    sysfont = pygame.font.SysFont("malgungothic", font_size)
    text = sysfont.render(text, True, color)  # WHITE = (255, 255, 255)

    screen.blit(text, (x, y))


# Input Text 세팅
input_id = InputBox(87, 57, 90, 32)
input_pw = InputBox(87, 123, 90, 32)
input_boxes = [input_id, input_pw]

while not done:
    # 메인 이벤트 루프
    for event in pygame.event.get():

        # 인풋 텍스트 박스 활성화
        if isLoginActivated:
            for box in input_boxes:
                box.handle_event(event)

        # 닫기 클릭 시
        if event.type == pygame.QUIT:
            done = True

        # 키보드 이벤트
        if event.type == pygame.KEYDOWN:

            # 로그인 화면에서 TAB(탭) 입력
            if event.key == pygame.K_TAB and not isCfActivated and not isUgActivated and not isUgResultActivated and isLoginActivated:
                print("Login - TAB ㅊ입력 : ID <-> PW Focus 전환")
                if isIdInputActivated:
                    isIdInputActivated = False
                else:
                    isIdInputActivated = True

            # 로그인 화면에서 ENTER(엔터) 입력
            if event.key == pygame.K_RETURN and not isCfActivated and not isUgActivated and not isUgResultActivated and isLoginActivated:
                print("Login - ENTER 입력 : 로그인")
                result = doLogin(input_id.text, input_pw.text)
                if result:
                    # 로그인 or 회원가입 성공
                    isFailToLogin = False
                    isLoginActivated = False
                    isHomeActivated = True
                else:
                    # 로그인 실패 : 비밀번호 불일치
                    isFailToLogin = True

            # F1 입력 : 힌트
            if event.key == pygame.K_F1 and not isCfActivated and not isUgActivated and not isUgResultActivated:
                if isHintActivated:
                    isHintActivated = False
                    clickSound.play()
                else:
                    isHintActivated = True
                    clickSound.play()

            # 스타포스 화면에서 SPACE BAR(스페이스바) 입력
            if event.key == pygame.K_SPACE and not isCfActivated and isUgActivated and not isUgResultActivated:
                print("Upgrade - SPACE BAR 입력 = STOP 클릭 ")
                clickSound.play()
                if 129 < starX < 177:
                    catchSound.play()
                    isSuccessCatch = True
                    print("스타캐치 성공")
                else:
                    isSuccessCatch = False

                # 강화 결과에 따른 강화 수치 변경
                # 스타캐치 설정 후 강화
                upgradeResult = startUpgrade()

                print(upgradeResult)

                isCfActivated = False
                isUgActivated = False
                isUgResultActivated = True

        # 마우스 이벤트
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("좌표 : ", pygame.mouse.get_pos())

            # 힌트(?) 클릭
            if not isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 305 <= \
                    mouse[0] <= 315 and 2 <= mouse[1] <= 14:
                print("Hint 버튼 클릭")
                isHintActivated = True
                clickSound.play()

            # 홈에서 강화 버튼 클릭 : 확인창 출력
            if not isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 81 <= \
                    mouse[0] <= 165 and 254 <= \
                    mouse[1] <= 273:
                print("Frame - 강화 클릭")
                isCfActivated = True
                clickSound.play()

            # 홈에서 취소 버튼 클릭 : 종료
            if not isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 173 <= \
                    mouse[0] <= 255 and 253 <= \
                    mouse[1] <= 272:
                print("Frame - 취소 클릭")
                clickSound.play()
                done = True

            if not isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 136 <= \
                    mouse[0] <= 149 and 198 <= \
                    mouse[1] <= 210:
                if not isNoStarCatch:
                    print("Frame - 스타캐치 해제 클릭")
                    isNoStarCatch = True
                else:
                    print("Frame - 스타캐치 해제 취소")
                    isNoStarCatch = False

            # 강화를 시도하시겠습니까? / 확인 버튼 클릭 이벤트
            if isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 86 <= mouse[
                0] <= 162 and 169 <= \
                    mouse[1] <= 189:
                print("Confirm - 확인 클릭")
                isCfActivated = False
                # 스타캐치 해제 체크 후 강화
                if isNoStarCatch:
                    upgradeResult = startUpgrade()

                    isUgResultActivated = True
                    print(upgradeResult)
                    print(isNoStarCatch, isUgResultActivated, isCfActivated, isUgActivated)
                # 스타캐치 화면으로 이동
                else:
                    isUgActivated = True

                clickSound.play()

            # 강화를 시도하시겠습니까? / 취소 버튼 클릭 이벤트
            if isCfActivated and not isUgActivated and not isUgResultActivated and not isHintActivated and 174 <= mouse[
                0] <= 252 and 169 <= \
                    mouse[1] <= 189:
                print("Confirm - 취소 클릭")
                isCfActivated = False
                isUgActivated = False
                clickSound.play()

            # 스타캐치 STOP 버튼 클릭 이벤트
            if not isCfActivated and isUgActivated and not isUgResultActivated and not isHintActivated and 123 <= mouse[
                0] <= 230 and 209 <= \
                    mouse[1] <= 258:
                print("Upgrade - STOP 클릭")
                clickSound.play()
                if 129 < starX < 177:
                    catchSound.play()
                    isSuccessCatch = True
                    print("스타캐치 성공")
                else:
                    isSuccessCatch = False

                # 강화 결과에 따른 강화 수치 변경
                # 스타캐치 설정 후 강화
                upgradeResult = startUpgrade()
                print(upgradeResult)

                isCfActivated = False
                isUgActivated = False
                isUgResultActivated = True
                clickSound.play()

            # 강화 결과 창 마우스 이벤트
            if not isCfActivated and not isUgActivated and isUgResultActivated and not isHintActivated and 128 <= mouse[
                0] <= 207 and 197 <= \
                    mouse[1] <= 218:
                print("Result - 확인 클릭")
                clickSound.play()
                isUgResultActivated = False

    # ######## 메인 이벤트 루프 끝

    # 로그인 화면
    if isLoginActivated and not isHomeActivated and not isCfActivated and not isUgActivated and not isHintActivated:

        for box in input_boxes:
            box.update()

        screen.blit(login, (0, 0))
        for box in input_boxes:
            box.draw(screen)

        if isIdInputActivated:
            input_id.active = True
            input_pw.active = False
        else:
            input_pw.active = True
            input_id.active = False

        if isFailToLogin:
            createText("PW 불일치 (신규 사용자라면 이미 존재하는 ID)", 13, 35, 171, RED)

        createText("도움말 F1", 15, 260, 1, BLACK)

    # 홈 화면
    if isHomeActivated and not isCfActivated and not isUgActivated and not isHintActivated:
        screen.blit(frame, (0, 0))
        createText("+" + str(current_ug) + "성 → " + "+" + str(current_ug + 1) + "성", 15, 137, 92, WHITE)
        createText("성공 : " + str(general_percentages['star_' + str(current_ug + 1)][0]) + "%", 15, 137, 121, WHITE)
        createText("유지 : " + str(general_percentages['star_' + str(current_ug + 1)][1]) + "%", 15, 224, 121, WHITE)
        createText("하락 : " + str(general_percentages['star_' + str(current_ug + 1)][2]) + "%", 15, 137, 157, WHITE)
        createText("파괴 : " + str(general_percentages['star_' + str(current_ug + 1)][3]) + "%", 15, 224, 157, WHITE)
        createText("스타캐치는 SPACE 키로도 가능해요", 12, 112, 223, WHITE)
        createText("랭킹 : 전체 유저 " + str(total_user) + "명 중 " + str(current_user_ranking) + "등", 12, 30, 55, WHITE)
        if isNoStarCatch:
            createText("v", 20, 138, 188, BLACK)
        else:
            createText("V", 1, 136, 188, WHITE)

        # 강화 결과 창
        if isUgResultActivated:
            if upgradeResult == 'success':
                screen.blit(upgrade_success, (27, 75))
            elif upgradeResult == 'keep':
                screen.blit(upgrade_fail, (27, 75))
            elif upgradeResult == 'down':
                screen.blit(upgrade_down, (27, 75))
            elif upgradeResult == 'destroy':
                screen.blit(upgrade_destroy, (27, 75))

    # 힌트 화면
    elif isHintActivated:
        screen.blit(hint, (0, 0))

        if current_user_id == "":
            current_user_id = "[비로그인]"
        createText(current_user_id + " 님은 총 " + str(current_count_ug) + "번 강화했어요", 13, 25, 82, BLUE)
        createText("1. 도움말은 F1 키로 켜고 끌 수 있어요", 13, 25, 112, BLACK)
        createText("2. TAB : ID, PW 전환 / ENTER : 로그인 ", 13, 25, 142, BLACK)
        createText("3. 스타캐치 성공 시 보너스(3~5%)가 적용 돼요", 13, 25, 172, BLACK)
        createText("4. 스타캐치는 SPACE 키로도 가능해요", 13, 25, 202, BLACK)
        createText("5. 피드백은 언제든지 환영해요 - 구성우", 13, 25, 232, BLACK)

    # 강화 버튼 누른 후 확인창
    elif isCfActivated and not isUgActivated and not isHintActivated:
        screen.blit(frame, (0, 0))
        screen.blit(confirm, (27, 45))

    # 스타캐치 창
    elif not isCfActivated and isUgActivated and not isHintActivated:
        screen.blit(frame, (0, 0))
        screen.blit(upgrade, (35, 15))
        # 스타
        if starX > 252:
            starDirection *= -1

        if starX < 50:
            starDirection *= -1

        starX += starSpeed * starDirection
        screen.blit(star, (starX, starY))

    pygame.display.update()
    clock.tick(60)

    mouse = pygame.mouse.get_pos()

    # # hover
    # if 81 <= mouse[0] <= 165 and 254 <= mouse[1] <= 273:
    #   pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])

    # else:
    #   pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

# While 문 끝

pygame.quit()
