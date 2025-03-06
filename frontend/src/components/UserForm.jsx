import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import DialogBox from '@/components/templates/DialogBox'
import { useForm } from 'react-hook-form'
import { instance } from '@/../axiosConfig'
import { useState } from 'react'
import AlertBox from './templates/AlertBox'

const nameValidation = {
    required: 'Name is required.',
    minLength: {
        value: 3,
        message: 'Name must be at least 3 letters.'
    },
    maxLength: {
        value: 10,
        message: 'Name shouldn&apost exceed 10 letters'
    },
    pattern: {
        value: /[a-zA-Z]/,
        message: 'Name should only consists of letters'
    }
}

const passwordValidation = {
    required: 'Password is required.',
    minLength: {
        value: 6,
        message: 'Your password must be at least 6 characters.'
    },
    maxLength: {
        value: 18,
        message: 'Your password shouldn&apost exceed 18 characters'
    }
}

// function UserForm({ formId, setUserName = () => {}, buttonText }) {
function UserForm({ formId, buttonText, setUserName = () => {} }) {
    const { register, reset, handleSubmit, formState:{errors}} = useForm()
    const [isDialogOpen, setDialogOpen] = useState(false)
    const [alertText, setAlertText] = useState('')

    const onSubmit = async (data) => {
        const endpoint = (formId === 'login') ? '/token': '/signup'

        try {
            const response = await instance.post(endpoint,
                new URLSearchParams({
                    username: data.username,
                    password: data.password
                }),
                {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
                }
            )

            if (formId === 'login')
                sessionStorage.setItem('access_token', response.data.token.access_token)
                sessionStorage.setItem('name', response.data.name)
                setUserName(response.data.name)

            // console.log(response.data)

            setDialogOpen((prevState) => !prevState)

        } catch (error) {
            setAlertText(error.response?.data?.detail || error.message)
            // console.error(error)
        }
    }

    const resetDialogForm = () => {
        reset()
        setAlertText('')
    }

    return (
        <DialogBox 
            formId={formId} 
            reset={resetDialogForm} 
            isDialogOpen={isDialogOpen} 
            setDialogOpen={setDialogOpen}
            dialogBoxText={buttonText}

        >
            {alertText && (
                <AlertBox alertText={alertText} variant='destructive' />
            )}
            <form id={formId} onSubmit={handleSubmit(onSubmit)} autoComplete='off'>
                <div>
                    <Label htmlFor='username'>Name</Label>
                    <Input id='username' {...register('username', nameValidation)}></Input>
                    {errors.username && (
                        <p className='text-sm font-medium leading-none'>{errors.username.message}</p>
                    )}
                </div>
                <div>
                    <Label htmlFor='password'>Password</Label>
                    <Input 
                        id='password' 
                        type='password' 
                        {...register('password', passwordValidation)} 
                    />
                    {errors.password && (
                        <p className='text-sm font-medium leading-none'>{errors.password.message}</p>
                    )}
                </div>
                {formId !== 'login' && (
                    <div>
                        <Label htmlFor='confirm-password'>Confirm Password</Label>
                        <Input 
                            id='confirm-password' 
                            type='password' 
                            {...register('confirmPassword', {...passwordValidation,
                                validate: {
                                    passwordMatch: (passwordConfirm, formValues) => {
                                        return passwordConfirm === formValues.password || (
                                            'Passwords should match.'
                                        )
                                    }
                                }
                            })} 
                        />
                        {errors.confirmPassword && (
                            <p className='text-sm font-medium leading-none'>{errors.confirmPassword.message}</p>
                        )}
                    </div>
                )}
            </form>
        </DialogBox>
    )
}

export default UserForm