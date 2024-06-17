const backendUrl = import.meta.env.VITE_BACKEND_URL as string;

export const initiateConversationUrl = backendUrl + '/initiateConversation/'
export const promptUrl = backendUrl + '/prompt/'