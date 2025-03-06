import { Button } from '@/components/ui/button'
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogTitle,
    DialogDescription,
    DialogHeader,
    DialogFooter,
} from '@/components/ui/dialog'

function DialogBox({ formId = '', reset, isDialogOpen, setDialogOpen, dialogBoxText, children }) {
    const onDialogOpenChange = (open) => {
        setDialogOpen(open)

        if (!open) {
            setTimeout(() => {
                reset();
            }, 100);
        }
    }

    return (
        <Dialog open={isDialogOpen} onOpenChange={onDialogOpenChange} >
            <DialogTrigger asChild>
                <Button variant='ghost'>{dialogBoxText}</Button>
            </DialogTrigger>
            <DialogContent className='sm:max-w-[425px]'>
                <DialogHeader>
                    <DialogTitle>{dialogBoxText}</DialogTitle>
                    <DialogDescription>Enter your name and password.</DialogDescription>
                </DialogHeader>
                <div className='py-4'>
                    {children}
                </div>
                <DialogFooter>
                    <Button type='submit' form={formId}>Submit</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
    }

export default DialogBox