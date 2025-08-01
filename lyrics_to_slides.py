#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
가사를 Google Slides로 자동 변환하는 프로그램
"""

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def setup_google_services():
    """Google API 서비스 설정"""
    # GitHub Secrets에서 인증 정보 가져오기
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not credentials_json:
        raise ValueError("Google 인증 정보가 없습니다!")
    
    # JSON 문자열을 딕셔너리로 변환
    credentials_info = json.loads(credentials_json)
    
    # Google API 인증
    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/presentations',
                'https://www.googleapis.com/auth/drive']
    )
    
    # Slides와 Drive 서비스 생성
    slides_service = build('slides', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    
    return slides_service, drive_service

def split_lyrics_into_pairs(lyrics_text):
    """가사를 두 줄씩 나누는 함수"""
    # 줄바꿈으로 분리
    lines = lyrics_text.strip().split('\n')
    
    # 빈 줄 제거
    lines = [line.strip() for line in lines if line.strip()]
    
    # 두 줄씩 묶기
    pairs = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            # 두 줄이 모두 있는 경우
            pairs.append(lines[i] + '\n' + lines[i + 1])
        else:
            # 마지막에 한 줄만 남은 경우
            pairs.append(lines[i])
    
    return pairs

def create_slides_presentation(slides_service, drive_service, title, lyrics_pairs):
    """Google Slides 프레젠테이션 생성"""
    
    # 1. 새 프레젠테이션 생성
    presentation = {
        'title': title
    }
    
    presentation = slides_service.presentations().create(body=presentation).execute()
    presentation_id = presentation['presentationId']
    
    print(f"✅ 프레젠테이션 생성 완료: {title}")
    print(f"📝 ID: {presentation_id}")
    
    # 2. 기본 슬라이드 삭제 (제목 슬라이드)
    requests = [
        {
            'deleteObject': {
                'objectId': 'p'  # 기본 슬라이드 ID
            }
        }
    ]
    
    # 3. 각 가사 쌍에 대해 슬라이드 생성
    for i, lyrics_pair in enumerate(lyrics_pairs):
        slide_id = f'slide_{i}'
        
        # 슬라이드 추가
        requests.append({
            'createSlide': {
                'objectId': slide_id,
                'slideLayoutReference': {
                    'predefinedLayout': 'BLANK'  # 빈 레이아웃
                }
            }
        })
        
        # 텍스트 박스 추가
        text_box_id = f'textbox_{i}'
        requests.append({
            'createShape': {
                'objectId': text_box_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {'magnitude': 300, 'unit': 'PT'},
                        'width': {'magnitude': 600, 'unit': 'PT'}
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 100,
                        'translateY': 150,
                        'unit': 'PT'
                    }
                }
            }
        })
        
        # 텍스트 추가
        requests.append({
            'insertText': {
                'objectId': text_box_id,
                'text': lyrics_pair
            }
        })
        
        # 텍스트 스타일 설정 (흰색, 큰 글씨)
        requests.append({
            'updateTextStyle': {
                'objectId': text_box_id,
                'style': {
                    'foregroundColor': {
                        'opaqueColor': {
                            'rgbColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            }
                        }
                    },
                    'fontSize': {
                        'magnitude': 48,
                        'unit': 'PT'
                    },
                    'bold': True
                },
                'fields': 'foregroundColor,fontSize,bold'
            }
        })
        
        # 텍스트 정렬 (가운데)
        requests.append({
            'updateParagraphStyle': {
                'objectId': text_box_id,
                'style': {
                    'alignment': 'CENTER'
                },
                'fields': 'alignment'
            }
        })
        
        # 슬라이드 배경을 검은색으로 설정
        requests.append({
            'updatePageProperties': {
                'objectId': slide_id,
                'pageProperties': {
                    'pageBackgroundFill': {
                        'solidFill': {
                            'color': {
                                'rgbColor': {
                                    'red': 0.0,
                                    'green': 0.0,
                                    'blue': 0.0
                                }
                            }
                        }
                    }
                },
                'fields': 'pageBackgroundFill'
            }
        })
    
    # 4. 모든 변경사항 적용
    if requests:
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': requests}
        ).execute()
    
    print(f"✅ {len(lyrics_pairs)}개의 슬라이드 생성 완료!")
    
    # 5. 공유 링크 생성
    drive_service.permissions().create(
        fileId=presentation_id,
        body={
            'role': 'reader',
            'type': 'anyone'
        }
    ).execute()
    
    slides_url = f'https://docs.google.com/presentation/d/{presentation_id}/edit'
    
    return presentation_id, slides_url

def main():
    """메인 실행 함수"""
    try:
        # 1. Google 서비스 설정
        print("🔧 Google API 연결 중...")
        slides_service, drive_service = setup_google_services()
        
        # 2. 가사 파일 읽기
        lyrics_file = 'lyrics.txt'
        if not os.path.exists(lyrics_file):
            print(f"❌ 오류: {lyrics_file} 파일이 없습니다!")
            print("💡 lyrics.txt 파일에 가사를 입력해주세요.")
            return
        
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics_text = f.read()
        
        if not lyrics_text.strip():
            print("❌ 오류: 가사 파일이 비어있습니다!")
            return
        
        # 3. 가사를 두 줄씩 나누기
        print("📝 가사를 두 줄씩 나누는 중...")
        lyrics_pairs = split_lyrics_into_pairs(lyrics_text)
        
        print(f"📊 총 {len(lyrics_pairs)}개의 슬라이드가 생성됩니다.")
        
        # 4. 프레젠테이션 제목 설정
        title = "가사 프롬프터"
        
        # 5. Google Slides 생성
        print("🎨 Google Slides 생성 중...")
        presentation_id, slides_url = create_slides_presentation(
            slides_service, drive_service, title, lyrics_pairs
        )
        
        # 6. 결과 출력
        print("\n🎉 완료!")
        print(f"📑 프레젠테이션 제목: {title}")
        print(f"🔗 링크: {slides_url}")
        print(f"📱 슬라이드 수: {len(lyrics_pairs)}개")
        
        # GitHub Actions에서 결과를 쉽게 확인할 수 있도록 파일로 저장
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write(f"프레젠테이션 링크: {slides_url}\n")
            f.write(f"슬라이드 수: {len(lyrics_pairs)}개\n")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return

if __name__ == "__main__":
    main()
