import ChatBox from '@/components/ChatBox'
import MessageBox from '@/components/MessageBox'
import NavBar from '@/components/NavBar'
import { ws_instance } from '@/../axiosConfig'
import { useEffect, useState } from 'react'
import { toast } from 'sonner'

function getStoredName() {
    return sessionStorage.getItem('name')
}

const STORED_NAME = getStoredName()

function ChatUI() {
    const [webSocket, setWebSocket] = useState(null)
    const [userName, setUserName] = useState(STORED_NAME)

    const handleWebSocketClose = () => {
        if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.close(1000)
        }
    }

    useEffect(() => {
        if (!userName) return

        const ws = new WebSocket(`${ws_instance}/chat`)

        ws.onopen = () => {
            const token = sessionStorage.getItem('access_token')
            // console.log(`Web Socket connection is open. Access token: ${token}`)
            const payload = JSON.stringify({access_token: token})

            ws.send(payload)
        }
        ws.onerror = (event) => {toast('Login Failed', {
            description: event.reason
        })}

        // ws.onclose = () => console.log('Web Socket connection is closing.')
        ws.onclose = (event) => {
            if (event.code != 1000) {
                toast('Login Failed', {
                    description: event.reason
                })
            }
            setWebSocket(null)
            setUserName(null)
            sessionStorage.removeItem('name')
            sessionStorage.removeItem('access_token')
        }

        setWebSocket(ws)
        
        return () => {
            // console.log('closing')
            ws.close(1000)
            // handleWebSocketClose()
        }
    }, [userName])

    return (
        <div className='flex flex-col h-screen'>
            <NavBar userName={userName} setUserName={setUserName} handleDisconnect={handleWebSocketClose} />
            {webSocket ? (
                <>
                    <MessageBox webSocket={webSocket} userName={userName} /> 
                    <ChatBox webSocket={webSocket} />
                </>) : (
                    <p className='text-lg text-muted-foreground'>Login to see messages.</p>
                )
            }
        </div>
    )
}

export default ChatUI