import { View, TextInput, Text } from "react-native";
import { useState } from "react";

/* type Chat = {
    msg: string -> <user_request> | <bot_reponse>;
    type: string -> 'user' | 'bot';
} */

const App = () => {
    const [inputText, setInputText] = useState('');
    const [chatLogs, setChatLogs] = useState([]);

    const addText = () => {
        // User part
        const newChat = { msg: inputText, type: "user" }

        setChatLogs(prevLogs => {
            return [...prevLogs, newChat]
        })

        setInputText('')
    }

    return (
        <View className='h-full px-5 py-16'>
            <View>
                <TextInput 
                    className='px-3 py-3 border border-[#CCCCCC] rounded-2xl mb-5 bg-[#F5F5F5]'
                    placeholder="Type here"
                    defaultValue={inputText}
                    onChangeText={newText => setInputText(newText)}
                    onSubmitEditing={addText}
                />

                {chatLogs && chatLogs.map((chat, index) => (
                    <View key={index} className={`${chat.type === 'user' ? 'self-end bg-[#2294fb]' : 'self-start bg-[#5A5A5A]'} mt-2 px-3.5 py-2.5 rounded-3xl`}>
                        <Text className='text-white leading-5 text-base'>{chat.msg}</Text>
                    </View>
                ))}
            </View>
        </View>
    )
}

export default App;
