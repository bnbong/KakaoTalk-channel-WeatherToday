class ForecastDataTrimmer():

    def __init__(self):
        self.category_list = {"TMP":"1시간 기온", "TMN":"일 최저 기온", "TMX":"일 최고 기온", "POP":"강수확률",
        "PTY":"강수형태", "PCP":"1시간 강수량", "REH":"습도", "UUU":"풍속(동서성분)", "VVV":"풍속(남북성분)",
        "VEC":"풍향", "WSD":"풍속", "SKY":"하늘상태", "WAV":"파고", "SNO":"1시간 신적설"}
        self.category_short = None
        self.category_long = None
        self.weather_value = None

    def category_converter(self, data):
        # this bot will provide SNO, POP, TMX, TMN, PTY, PCP, REH, WSD, SKY information.

        self.category_short = data.get('category')
        self.category_long = self.category_list.get(self.category_short)
        self.calculate_weather_value(self.category_short, data.get('fcstValue'))

    def calculate_weather_value(self, category, fcstValue):
        match category:
            case "PCP" :
                self.pcp_calculator(fcstValue)
            case "SNO":
                self.sno_calculator(fcstValue)
            case "POP":
                self.pop_calculator(fcstValue)
            case "SKY":
                self.sky_calculator(fcstValue)
            case "WSD":
                self.wsd_calculator(fcstValue)
            case "TMN":
                self.tmn_calculator(fcstValue)
            case "TMX":
                self.tmx_calculator(fcstValue)
            case "PTY":
                self.pty_calculator(fcstValue)
            case "REH":
                self.reh_calculator(fcstValue)

    def pcp_calculator(self, value):
        if value == "강수없음":
            self.weather_value = value
        elif float(value) < (float)(1.0):
            self.weather_value = "1.0mm 미만"
        elif float(value) < (float)(30.0):
            self.weather_value = "1.0 ~ 29.0mm"
        elif float(value) < (float)(50.0):
            self.weather_value = "30.0 ~ 50.0mm"
        else:
            self.weather_value = "50.0mm 이상"

    def sno_calculator(self, value):
        if value == "적설없음":
            self.weather_value = value
        elif float(value) < (float)(1.0):
            self.weather_value = "1.0cm 미만"
        elif float(value) < (float)(5.0):
            self.weather_value = value + "cm"
        else:
            self.weather_value = "5.0cm 이상"

    def pop_calculator(self, value):
        self.weather_value = "강수확률 : " + value + "%"

    def tmn_calculator(self, value):
        self.weather_value = "최저기온" + value + "C"

    def tmx_calculator(self, value):        
        self.weather_value = "최고기온" + value + "C"

    def pty_calculator(self, value):
        match value:
            case 0:
                self.weather_value = "강수 없음"
            case 1:
                self.weather_value = "비"
            case 2:
                self.weather_value = "비 또는 눈"
            case 3:
                self.weather_value = "눈"
            case 4:
                self.weather_value = "소나기"

    def reh_calculator(self, value):
        self.weather_value = "습도 : " + value + "%"

    def wsd_calculator(self, value):
        if float(value) < 4:
            self.weather_value = "약한 바람"
        elif float(value) < 9:
            self.weather_value = "약간 강한 바람"
        elif float(value) < 14:
            self.weather_value = "강한 바람"
        else:
            self.weather_value = "매우 강한 바람"

    def sky_calculator(self, value):
        if int(value) < 6:
            self.weather_value = "맑음"
        elif int(value) < 9:
            self.weather_value = "구름많음"
        else:
            self.weather_value = "흐림"
    