import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import LoginState from "@/components/loginstate";
import style from "@/pages/reg/forgetpassword.module.css"
/*
	未登入使用者忘記密碼，跳轉到此頁面可以輸入信箱寄出驗證碼驗證

*/
export default function ForgetPassword() {
    const [email, setEmail] = useState("");
    const [validationNum, setValidationNum] = useState("");
    const [message, setMessage] = useState("");
	const [ErrorMessage, setErrorMessage] = useState("");
    const [countdown, setCountdown] = useState(60);
    const [buttonEnabled, setButtonEnabled] = useState(true);
	const [valSuccess, setValSuccess] = useState(false);
	const [valEnabled, setValEnabled] = useState(false);

	/* 已經驗證完後需要的 */
	const [password, setPassword] = useState("");   // 第一次密碼
    const [password_check, setPassword_Check] = useState("");   // 確認密碼
    const [passwordsLegth, setpasswordsLegth] = useState(false); // 用於檢查密碼長度
    const [passwordsMatch, setPasswordsMatch] = useState(false); // 用於檢查密碼匹配
	const router = useRouter();

	const resetPaawordEmailClick = async(e) => {
		/* 按下修改密碼的按鍵的onClick */

		try{
			const response = await fetch("http://127.0.0.1:8000/reg/api/resetpassword", {
				method:"POST",
				body : JSON.stringify({email, password}),
				headers:{
					"Content-Type": "application/json",
				}
	
			});
			if(response.status === 200){
				const responceData = await response.json();
				console.log(responceData.message);
				router.push(responceData.redirect);
			} else {
				/* 應該不會發生 */
				const responceData = await response.json();
				console.log(responceData.message);
			}
		} catch (error) {
			console.log(error);
		}
		
	}

	// 在password和password_check改變時檢查密碼是否匹配
	const handlePasswordLegthCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword(confirmPassword);
        setPasswordsMatch(false)
        const isPasswordLegthEnought = confirmPassword.length >= 6;
        setpasswordsLegth(isPasswordLegthEnought);
		const isPasswordMatch = confirmPassword === password_check && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
    };

    // 在password和password_check改變時檢查密碼是否匹配
    const handlePasswordCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword_Check(confirmPassword);
        const isPasswordMatch = confirmPassword === password && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
    };
	useEffect(() => {
		let countdownInterval;

		if (countdown > 0 && !buttonEnabled) {
			countdownInterval = setInterval(() => {
				setCountdown(countdown - 1);
				setMessage(`您還有 ${countdown-1} 秒可以重新寄送郵件。`);
			}, 1000);
		} else {
			clearInterval(countdownInterval);
			setButtonEnabled(true);
			setCountdown(60);
			setMessage(`您還有 ${countdown} 秒可以重新寄送郵件。`);
		}

		return () => {
			clearInterval(countdownInterval);
		};
	}, [countdown, buttonEnabled]);

  const hadsendValnumClick = async (e) =>{
	e.preventDefault();
	const validation_numPattern = /^\d{6}$/
	if (!validation_numPattern.test(validationNum)){
		setErrorMessage("請輸入有效的驗證碼！");
		return;
	} else {
		setErrorMessage("");
	}
	try{
		const response = await fetch("http://127.0.0.1:8000/reg/api/valdatae", {
			method : "POST",
			body : JSON.stringify({ email, validationNum }),
			headers: {
				"Content-Type": "application/json",
			  },
		})

		if (response.status === 200){
			const responseData = await response.json();
			console.log(`${responseData.message}`);
			setValSuccess(true);
		} else {
			const responseData = await response.json();
			setErrorMessage(responseData.message);
		}
	} catch (error){
		console.log(error);
	}

  };
  const handleSendEmailClick = async (e) => {
	e.preventDefault();

	// 驗證電子郵件地址格式
	const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
	if (!emailPattern.test(email)) {
		setErrorMessage("請輸入有效的電子郵件地址！");
		return;
	}
	setErrorMessage("");
    setButtonEnabled(false);
	setValEnabled(true);
    setCountdown(60);
    try{
		const response = await fetch("http://127.0.0.1:8000/reg/api/forgetpwdvalresend", {
			method : "POST",
			body : JSON.stringify({ email }),
			headers: {
				"Content-Type": "application/json",
			  },
		})

		if (response.status === 200){
			const responseData = await response.json();
			console.log(responseData);

		} else {
			const responseData = await response.json();
			console.log(responseData.message);
			setErrorMessage(responseData.message)
		}
    } catch (error){
		console.error(error)
    }
  };

  return (
    <>
		<Head>
			<title>忘記密碼</title>
		</Head>
		<LoginState
            profilePath="../../ifm"
            resetPasswordPath="./"
            logoutPath=""
        />
		{/* 進入網站未發送郵件前 */}
		{!valSuccess && <div className="novaldate">
			<div className={style.forgetpwdpagecontainer}>
				<div className={style.formcontainer}>
					<div className="emailcontainer">
						<label htmlFor="email">電子郵件:</label>
						<input
							type="text"
							id="email"
							name="email"
							required
							value={email}
							onChange={(e) => setEmail(e.target.value)}
						/>
					</div>
					<button
						className={style.button}
						id="button"
						onClick={handleSendEmailClick}
						disabled={!buttonEnabled}
						>
						發送郵件
					</button>
					{!buttonEnabled && <div style={{ color: "red" }} className={style.errormsg}>{message}</div>}
					{valEnabled && 
						<div className="validation_container">
							<label htmlFor="validationNum">驗證碼:</label>
							<input
								type="number"
								id="validationNum"
								name="validation_num"
								required
								value={validationNum}
								onChange={(e) => setValidationNum(e.target.value)}
							/>

							<button 
								className={style.sendValdationnum} 
								id="button"
								onClick={hadsendValnumClick}
							>
							驗證
							</button>
						</div>
						
						
					}
				{ErrorMessage && <div style={{color:"red"}} className={style.errormsg}>{ErrorMessage}</div>}
				</div>
				
			</div>
		</div>}

		{valSuccess && 
		<div className={style.resetpwdpagecontainer}>
			<div className={style.resetpwdpageformcontainer}>
				<div className="emailcontainer">
					<label>電子郵件:</label>
					<input
						type = "email"
						defaultValue = {email}
						disabled = 'false'
					/>
				</div>
				<div className="passwordcontainer">
					<label htmlFor="email">密碼:</label>
					<input
						type="password"
						id="password" name="password"
						required
						value={password}
						onChange={handlePasswordLegthCheckChange}
					/>
					{passwordsLegth && <span style={{ color: "green" }} className={style.errormsg}> &#10003; </span>}
					{!(passwordsLegth) && <span style={{ color: "red" }} className={style.errormsg}> 密碼長度不足 </span>}
				</div>
				
				<div className="passwordcontainer">
					<label htmlFor="password">確認密碼:</label>
					<input
						type="password"
						id="password_check" name="password_check"
						required
						value={password_check}
						onChange={handlePasswordCheckChange}
					/>
					{passwordsMatch && <span style={{ color: "green" }} className={style.errormsg}> &#10003; </span>}
					{!(passwordsMatch) && <span style={{ color: "red" }} className={style.errormsg}> 與密碼不相符 </span>}
				</div>
				
				<button
					className={style.button2}
					onClick={resetPaawordEmailClick}
					disabled={!passwordsMatch}
				>
					修改密碼
				</button>
				
			</div>
			
		</div>}
	
    </>
  );
}
