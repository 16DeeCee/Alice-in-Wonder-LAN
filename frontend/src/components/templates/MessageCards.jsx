import { Card, CardContent } from '@/components/ui/card'

function MessageCards({ msgList, ...props }) {
    return (
        <div {...props}>
            {msgList.map((message, id) => (
                <Card className={`flex-1 mb-2 bg-[#E4E4E7] border-[#D4D4D8] shadow-md w-fit max-w-[75%]`} id='msg' key={id}>
                    <CardContent className='p-3'>
                        {message}
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}

export default MessageCards