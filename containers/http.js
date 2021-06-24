const http = require("http") // 노드 모듈을 가져온다

const hostname = "127.0.0.1" // 사용할 서버 호스트네임
const port = 8080 // 사용할 서버 포트

// 서버를 만든다
const server = http.createServer((req, res) => {
  // 요청이 오면 실행되는 콜백 함수
  res.statusCode = 200 // 응답 상태값 설정
  res.setHeader("Content-Type", "text/plain") // 응답 헤더 중 Content-Type 설정
  res.end("Hello, World!\n") // 응답 데이터 전송
})

// 서버를 요청 대기 상태로 만든다
server.listen(port, hostname, () => {
  // 요청 대기가 완료되면 실행되는 콜백 함수
  // 터미널에 로그를 기록한다
  console.log(`Server running at http://${hostname}:${port}/`)
})
