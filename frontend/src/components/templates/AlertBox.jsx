import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import { AlertCircle  } from 'lucide-react'

function AlertBox({ alertTitle = 'Error', alertText, ...props }) {
    const AlertIcon = () => {
        if ('variant' in props && props.variant == 'destructive')
            return <AlertCircle className='h-5 w-5 my-1' />
    }

    return (
        <Alert {...props}>
            <AlertIcon />
            <AlertTitle>{alertTitle}</AlertTitle>
            <AlertDescription>
                {alertText}
            </AlertDescription>
        </Alert>
    )
}

export default AlertBox