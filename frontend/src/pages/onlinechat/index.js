import { useEffect, useState, useRef } from 'react';
import Style from '@/pages/onlinechat/css/index.module.css';
import LoginState from '@/components/loginstate';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Image from 'next/image';

const Lobby = () => {
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const messagesRef = useRef(null); // 創建一個ref 用來把視窗滾到最新訊息
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [chatSocket, setChatSocket] = useState(null);
    const router = useRouter();
    const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL;

	// 使用者點擊回覆的頭像，可以看到其他使用者的profile
	const [headiImageURL, setHeadiImageURL] = useState("");
    const [describe, setDescribe] = useState("");
    const [username, setUsername] = useState("");
	const [anotherUserClick, setAnotherUserClick] = useState(false);

	const GetAnotherUserProfile = async(username) => {
		if (username === '我沒有登入') {
			return;
		}
		const response = await fetch(`${backedUrl}/ifm/api/getanothoruserprofile`, {
			method:'POST',
			body:JSON.stringify(username),
			headers:{
				'Content-Type':'application/json',
			}
		});

		try {
			if (response.status === 200) {
				const responseData = await response.json();
				// console.log(responseData);
				setHeadiImageURL(responseData.headiImageURL);
				setDescribe(responseData.describe);
				setUsername(responseData.username);
				setAnotherUserClick(true);
			} else {
				const responseData = await response.json();
				// console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}

	const closeProfile = () =>{
		setAnotherUserClick(false);
	} 


    useEffect(() => {
      let socket = new WebSocket(`${socketUrl}/ws/socket-server/`);

      socket.onopen = () => {
        // console.log('WebSocket connected');
      };

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.redirect) {
        // console.log(data.redirect);
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
		  	{anotherUserClick && <div className={Style.mask} onClick={()=>closeProfile()}></div>}
			{anotherUserClick &&
			<div className={Style.profilecard}>
				<div className={Style.imagecontainer}>
					<Image
						src={ headiImageURL }
						alt="頭圖"
						height={45}
						width={45}
						priority
					/>
				</div>
				<div className={Style.textcontainer}>
					<div className={Style.username}><span style={{fontSize:'30px'}}>{ username }</span></div>
					<div className={Style.describe}><textarea defaultValue={describe} disabled/></div>
				</div>
			</div>}
			<form className={Style.textarea}>
				<div className={Style.messages} ref={messagesRef}>
				{messages.map((data, index) => (
					<div className={Style.chat_container} key={index}>
						<div className={Style.uppercontainer}>
							<img className={Style.headimg} src={`${backedUrl}/ifm${data.headimg}`} alt="User Avatar" 
								onClick={()=>GetAnotherUserProfile(data.username)}
							/>
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
