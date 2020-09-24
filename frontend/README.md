# frontend

vue.js 사용
Login view, Chat view 2개의 view가 있고 router에서 인증되어 있지 않으면 login view를 보여주고 인증 완료시 Chat view로 redirect 
Chat view는 ChatRoom과 RoomList 2개의 component로 구성.
ChatRoom은 실제 1:1 대화를 보여주는 component.
RoomList는 1:1 대화 목록 component.

login 요청 보낸후 발급받은 jwt localStorage에 넣어두고 다른 api요청시 사용
채팅 메세지는 websocket을 사용해서 주고 받음.

## deploy
- .env.local에 api base, ws base설정
  - VUE_APP_API_BASE
  - VUE_APP_WS_BASE
- yarn build
- nginx로 static file serve
  - vue-router에서 history mode쓰니까 index아닌경우에도 index.html내려줘야함

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
