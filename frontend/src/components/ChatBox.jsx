import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { SendHorizonal } from 'lucide-react'
import { useRef } from 'react'
// import webSocket from '@/lib/websocket.config'

function ChatBox({ webSocket }) {

    const messageRef = useRef(null)

    const sendMessage = () => {
        const message = messageRef.current.value
        if (message.trim()) {
            const payload = JSON.stringify({message})
            webSocket.send(payload)
            messageRef.current.value = ''
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className='mx-5 flex items-center gap-2 m-1'>
            <Textarea
                ref={messageRef}
                placeholder='Type a message' 
                rows={1}
                onKeyDown={handleKeyPress}
                disabled={!webSocket}
            />
            <Button 
                onClick={sendMessage} 
                variant='outline' 
                className='h-[2.5rem] w-[2.5rem]'
                disabled={!webSocket}
            ><SendHorizonal/></Button>
        </div>
    )
}

export default ChatBox
