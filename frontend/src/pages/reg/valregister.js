/*

    棄用

*/

import { useEffect, useState } from "react";

export default function Valregister(){
    const [valnum, setValnum] = useState(0);
    const [legel, setLegel] = useState(false);
    const [errerMessage, setErrerMessage] = useState();

    useEffect(()=>{

        if (valnum.toString().length === 6) {
            setErrerMessage('');
            console.log('長度足夠');
            setLegel(true);
        } else {
            setErrerMessage('不符合驗證碼長度限制');
            console.log('不符合長度要求限制');
            setLegel(false);
        }

    }, [valnum])
    return(
        <>  
            <label>驗證碼</label>
            <input
                type="number"
                onChange={(e)=>setValnum(e.target.value)}
            />
            <br/>
            <button
                disabled={!legel}
                
            >
                點擊驗證
            </button>
            {errerMessage && 
            <>

                <p style={{color:'red'}}>{errerMessage}</p>
            
            </>}
        </>
    );
}
