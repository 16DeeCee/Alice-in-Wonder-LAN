import { Label } from '@/components/ui/label'
import { ScrollArea } from '@/components/ui/scroll-area'
import MessageCards from '@/components/templates/MessageCards'
import { useEffect, useState, useRef } from 'react'

const UserMessages = ({ messages, userName = '' }) => (
    <>
        {messages.map((user, id) => {
            let alignItem
            let displayedName

            if (user.name === userName) {
                alignItem = 'items-end'
                displayedName = 'You'
            } else {
                alignItem = 'items-start'
                displayedName = user.name
            }
                
            return (
                <div key={id} className='mx-5 my-3'>
                    <div className={`flex flex-col ${alignItem}`}>
                        {/* Label for the user */}
                        <Label htmlFor={`${user.name}-${id}`} className='mb-1'>
                            {displayedName}
                        </Label>
                        <MessageCards 
                            msgList={user.message} 
                            id={`${user.name}-${id}`} 
                            className={`flex flex-col w-full ${alignItem}`}
                        />

                    </div>
                </div>
            )
        })}
    </>
);


function MessageBox({ webSocket, userName }) {
    const [messages, setMessages] = useState([])
    const scrollAreaRef = useRef(null)

    useEffect(() => {
        if (!webSocket) return

        webSocket.onmessage = (event) => {
            const newMessages = JSON.parse(event.data)
            // console.log(newMessages)
    
            setMessages((prevMessages) => {
                const messageHistory = [...prevMessages]
                const messageArray = Array.isArray(newMessages) ? newMessages : [newMessages]

                messageArray.forEach((newMessage) => {
                    const lastIndex = messageHistory.length - 1

                    if (messageHistory.length > 0 && messageHistory[lastIndex].name === newMessage.name) {
                        messageHistory[lastIndex].message.push(newMessage.message)
                    } else {
                        messageHistory.push({
                            name: newMessage.name,
                            message: [newMessage.message],
                        })
                        // console.log('adding new user.')
                    }
                })

                return messageHistory
            })
        }
    }, [webSocket])

    useEffect(() => {
        scrollAreaRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end'})
    }, [messages])
    // scrollAreaRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end'})

    return (
        <div className='flex overflow-y-auto'>
            <ScrollArea>
                <div ref={scrollAreaRef}>
                    {messages.length > 0 ? <UserMessages messages={messages} userName={userName} /> : <p>No messages yet.</p>}
                </div>
            </ScrollArea>
        </div>
    )
}

export default MessageBox