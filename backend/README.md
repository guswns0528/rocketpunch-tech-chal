# backend

## TODO
- [ ] 설정 분리
  - [ ] backend.settings.SECRET_KEY 
  - [ ] backend.settings.DEBUG
  - [ ] backend.settings.CHANNEL_LAYERS
- [ ] websocket message 보낼때 channel 살아 있는지 확인 필요
- [ ] chatroom 리스트 줄때 마지막 메세지가 최신인 방이 위에오도록 정렬
- [ ] message 읽었는지 여부 frontend에서 체크
- [ ] websocket으로 chat message 오면 sanitize해야함

## deploy
- backend/override_settings.py에 DATABASES 설정 넣기
- 로컬에 redis띄우기
- daphne -b 0.0.0.0 -p PORT backend.asgi:application
