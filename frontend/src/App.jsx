import ChatUI from '@/pages/ChatUI'
import { Toaster } from 'sonner'

function App() {
    return (
        <>
            <ChatUI/>
            <Toaster closeButton position='top-center' />
        </>
    )
}

export default App