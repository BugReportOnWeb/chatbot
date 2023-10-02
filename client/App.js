import { View, TextInput, Text } from "react-native";
import { useState } from "react";

const App = () => {
    const [inputText, setInputText] = useState('');
    const [chatLogs, setChatLogs] = useState([]);

    // type Chat = {
    //     msg: string -> <user_request> | <bot_reponse>;
    //     type: string -> 'user' | 'bot';
    // }

    const addChat = (chat) => {
         setChatLogs(prevLogs => {
            return [...prevLogs, chat]
        })       
    }

    const handleTextSubmit = async () => {
        // User request (UI display)
        const newUserChat = { msg: inputText, type: 'user' }
        addChat(newUserChat)
        setInputText('')

        // Bot response (Feching + UI display)
        try {
            const res = await fetch("http://172.20.10.2:8000", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ msg: newUserChat.msg })
            });

            const data = await res.json();
            const newBotChat = { msg: data.msg, type: 'bot' }

            addChat(newBotChat)
        } catch (err) {
            console.error(err);
        }
    }

    return (
        <View className='h-full px-5 py-16'>
            <View>
                <TextInput 
                    className='px-3 py-3 border border-[#CCCCCC] rounded-2xl mb-5 bg-[#F5F5F5]'
                    placeholder="Type here"
                    defaultValue={inputText}
                    onChangeText={newText => setInputText(newText)}
                    onSubmitEditing={handleTextSubmit}
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
