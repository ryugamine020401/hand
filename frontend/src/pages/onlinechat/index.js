import { useEffect, useState, useRef } from 'react';
import Style from '@/pages/onlinechat/index.module.css';

const Lobby = () => {
    const messagesRef = useRef(null); // 創建一個ref 用來把視窗滾到最新訊息
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [chatSocket, setChatSocket] = useState(null);

  useEffect(() => {
    let socket = new WebSocket(`ws://127.0.0.1:8000/ws/socket-server/`);

    socket.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.redirect) {
        console.log(data.redirect);
        window.location.href = data.redirect;
      } else if (data.type === 'chat') {
        setMessages([...messages, data]);
      }
    };

    setChatSocket(socket); // 設置 chatSocket 狀態
    scrollToBottom();
    return () => {
      if (chatSocket) {
        chatSocket.close();
      }
    };
  }, [messages]); // 只在 messages 更新時重新連接 WebSocket

  const scrollToBottom = () => {
    if (messagesRef.current) {
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  };

    const handleSubmit = (e) => {
        e.preventDefault();
        const message = newMessage.trim(); // 移除消息的前後空格
        if (message){
            if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
                const message = newMessage;
                chatSocket.send(JSON.stringify({
                    message,
                }));
                setNewMessage('');
            }
        }
    };

  return (
    <div>
      <h1>Online ChatRoom!</h1>
      <form className={Style.textarea}>
        <div className={Style.messages} ref={messagesRef}>
          {messages.map((data, index) => (
            <div className={Style.chat_container} key={index}>
              <div className={Style.headimgcontainer}>
                <img className={Style.headimg} src={`http://127.0.0.1:8000/ifm${data.headimg}`} alt="User Avatar" />
                <p className={Style.user_name}>{data.username}</p>

              </div>
              <p className={Style.userMessage}>{data.message}</p>
            </div>
          ))}
        </div>
      </form>
      <form className={Style.form} onSubmit={handleSubmit}>
        <input
          type="text"
          name="message"
          className="input"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Lobby;


// import Head from 'next/head'
// import {useEffect, useState} from "react";
// import Pusher from "pusher-js";

// export default function Home() {
//     const [username, setUsername] = useState('username');
//     const [messages, setMessages] = useState([]);
//     const [message, setMessage] = useState('');
//     let allMessages = [];

//     useEffect(() => {
//         Pusher.logToConsole = true;

//         const pusher = new Pusher('b1ec4bebf19fae50238a', {
//           cluster: 'ap3'
//         });
    
//         const channel = pusher.subscribe('chat');
//         channel.bind('message', function(data) {
//           // alert(JSON.stringify(data));
//           allMessages.push(data);
//           setMessages(allMessages);
//         });
//     });

//     const submit = async (e) => {
//         e.preventDefault();

//         await fetch('http://127.0.0.1:8000/onlinechat/api/message', {
//             method: "POST",
//             headers: {'Content-Type': 'application/json'},
//             body: JSON.stringify({
//                 username,
//                 message
//             })
//         });

//         setMessage('');
//     }

//     return (
//         <div className="container">
//             <Head>
//                 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet"
//                       integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x"
//                       crossOrigin="anonymous"/>
//             </Head>

//             <div className="d-flex flex-column align-items-stretch flex-shrink-0 bg-white">
//                 <div
//                     className="d-flex align-items-center flex-shrink-0 p-3 link-dark text-decoration-none border-bottom">
//                     <input className="fs-5 fw-semibold" value={username} onChange={e => setUsername(e.target.value)}/>
//                 </div>
//                 <div className="list-group list-group-flush border-bottom scrollarea" style={{minHeight: "500px"}}>
//                     {messages.map(message => {
//                         return (
//                             <div className="list-group-item list-group-item-action py-3 lh-tight" key={message.id}>
//                                 <div className="d-flex w-100 align-items-center justify-content-between">
//                                     <strong className="mb-1">{message.username}</strong>
//                                 </div>
//                                 <div className="col-10 mb-1 small">{message.message}</div>
//                             </div>
//                         )
//                     })}
//                 </div>
//             </div>

//             <form onSubmit={submit}>
//                 <input className="form-control" placeholder="Write a message" value={message}
//                        onChange={e => setMessage(e.target.value)}
//                 />
//             </form>
//         </div>
//     )
// }