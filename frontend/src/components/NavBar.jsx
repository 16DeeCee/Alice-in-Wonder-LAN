import { Button } from '@/components/ui/button'
import UserForm from '@/components/UserForm'

function NavBar({ userName, handleDisconnect, setUserName }) {
    return (
        <nav className='flex items-center justify-between px-6 py-4 border-b shadow-sm bg-background'>
            <div className='text-xl font-bold tracking-wide'>Chat</div>
                { !userName ? (
                    <div>
                        <UserForm formId='login' buttonText='Login' setUserName={setUserName} />
                        <UserForm formId='signup' buttonText='Signup' />
                    </div>) : (
                    <div className='text-xl font-bold tracking-wide'>
                        {userName}
                        <Button variant='ghost' onClick={() => handleDisconnect()}>Logout</Button>
                    </div>
                )}
        </nav>
    )
}

export default NavBar