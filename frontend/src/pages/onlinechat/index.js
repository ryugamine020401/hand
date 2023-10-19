import { useEffect, useState, useRef } from 'react';
import Style from '@/pages/onlinechat/css/index.module.css';
import LoginState from '@/components/loginstate';
import { useRouter } from 'next/router';
import Head from 'next/head';

const Lobby = () => {
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const messagesRef = useRef(null); // 創建一個ref 用來把視窗滾到最新訊息
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [chatSocket, setChatSocket] = useState(null);
    const router = useRouter();
    const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL;

  useEffect(() => {
    let socket = new WebSocket(`${socketUrl}/ws/socket-server/`);

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
				const access_token = localStorage.getItem('access_token');
				const message = newMessage;
				const messageData = {
					message: message,
					Authorization: `Bearer ${access_token}`, // header
				};
				chatSocket.send(JSON.stringify(messageData));

                // const message = newMessage;
                // chatSocket.send(JSON.stringify({
                //     message,
                // }));
                setNewMessage('');
            }
        }
    };

  return (
    
    <div>
      <Head><title>線上聊天室</title></Head>
		<LoginState
			profilePath="../ifm"
			resetPasswordPath="../reg/resetpassword"
			logoutPath="/uchi"
		/>
    
		<div className={Style.pagecontainer}>
      <button className={Style.repagebtn} onClick={()=>router.push('../uchi ')}>上一頁</button>
			<form className={Style.textarea}>
				<div className={Style.messages} ref={messagesRef}>
				{messages.map((data, index) => (
					<div className={Style.chat_container} key={index}>
						<div className={Style.uppercontainer}>
							<img className={Style.headimg} src={`${backedUrl}/ifm${data.headimg}`} alt="User Avatar" />
							<p className={Style.user_name}>{data.username}</p>
						</div>
						<div className={Style.lowercontainer}>
							<p className={Style.userMessage}>{data.message}</p>
						</div>
					</div>
				))}
				</div>
			</form>
			{/* <hr width="75%" color="blue"/> */}
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
    </div>
  );
};

export default Lobby;
