import { useState, useEffect } from "react";
import ButtonStyle from "./button.module.css";

export default function ForgetPassword() {
  const [email, setEmail] = useState("");
  const [validationNum, setValidationNum] = useState("");
  const [message, setMessage] = useState("");
  const [countdown, setCountdown] = useState(60);
  const [buttonEnabled, setButtonEnabled] = useState(true);

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

  const handleSendEmailClick = () => {
    setButtonEnabled(false);
    setCountdown(60); 
  };

  return (
    <main className="body">
      <h1>忘記密碼</h1>
      <label htmlFor="email">Email:</label>
      <input
        type="text"
        id="email"
        name="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <label htmlFor="validationNum">驗證碼:</label>
      <input
        type="text"
        id="validationNum"
        name="validationNum"
        required
        value={validationNum}
        onChange={(e) => setValidationNum(e.target.value)}
      />
      <br />
      <div id={ButtonStyle.buttoncontainer}>
        <button
          className="sendEmail"
          id={ButtonStyle.button}
          onClick={handleSendEmailClick}
          disabled={!buttonEnabled}
        >
          發送郵件
        </button>
        {!buttonEnabled && <span style={{ color: "red" }}>{message}</span>}
      </div>

      <div id={ButtonStyle.buttoncontainer}>
        <button className="sendEmail" id={ButtonStyle.button}>
          驗證
        </button>
      </div>
    </main>
  );
}
