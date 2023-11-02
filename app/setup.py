# TODO: install_requires 의존성 정의
# --------------------------------------------------------------------------
# Backend Application의 패키지 정보를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from setuptools import setup, find_packages

install_requires = [

]

# IDE will watch this setup config through your project src, and help you to set up your environment
setup(
    name="Kakao-WeatherToday",
    description="A weather forecasting KakaoTalk bot channel informs local weather.",
    author="bnbong",
    author_email="bbbong9@gmail.com",
    packages=find_packages(where="app"),
    use_scm_version=True,
    requires=["python (>=3.10)"],
    install_requires=install_requires,
)
