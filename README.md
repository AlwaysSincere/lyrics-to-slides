# 🎵 가사를 Google Slides로 자동 변환

라이브 공연 시 사용할 가사를 두 줄씩 나누어 검은 배경의 Google Slides로 자동 생성하는 시스템입니다.

## 🎯 기능
- ✅ 가사를 두 줄씩 자동 분할
- ✅ 검은 배경에 흰 글씨로 설정
- ✅ 큰 폰트 크기로 가독성 최적화
- ✅ 자동으로 공유 가능한 링크 생성
- ✅ 완전 무료 (GitHub Actions + Google API 무료 사용량)

## 🚀 사용 방법

### 방법 1: GitHub에서 직접 실행 (추천)
1. GitHub 저장소의 **Actions** 탭 클릭
2. **"가사를 Google Slides로 변환"** 워크플로우 선택
3. **"Run workflow"** 버튼 클릭
4. 텍스트 박스에 가사 입력
5. **"Run workflow"** 실행
6. 완료되면 **Google Slides 링크**를 확인!

### 방법 2: 파일로 업로드
1. `lyrics.txt` 파일 편집
2. 가사 입력 후 저장
3. GitHub에 푸시하면 자동으로 실행

## 📝 가사 입력 형식
```
첫 번째 줄
두 번째 줄
세 번째 줄  
네 번째 줄
다섯 번째 줄
여섯 번째 줄
```

**결과:**
- 슬라이드 1: "첫 번째 줄 + 두 번째 줄"
- 슬라이드 2: "세 번째 줄 + 네 번째 줄"  
- 슬라이드 3: "다섯 번째 줄 + 여섯 번째 줄"

## 🔧 초기 설정 (한 번만)
1. Google Cloud Console에서 API 활성화
2. 서비스 계정 생성
3. GitHub Secrets에 인증 정보 저장

## 📱 결과 확인
- Actions 완료 후 **Artifacts** 섹션에서 `slides-result` 다운로드
- `result.txt` 파일에서 Google Slides 링크 확인

## 🎨 슬라이드 스타일
- **배경:** 검은색 (#000000)
- **글씨:** 흰색 (#FFFFFF)
- **폰트 크기:** 48pt
- **정렬:** 가운데
- **굵기:** 굵게

## 🆘 문제 해결
- **"GOOGLE_CREDENTIALS 오류"**: GitHub Secrets 설정 확인
- **"가사 파일 없음"**: lyrics.txt 파일 생성 확인
- **"권한 오류"**: Google API 권한 설정 확인

## 📞 지원
문제가 발생하면 Issues 탭에서 문의해주세요!
