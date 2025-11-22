export const API_ENDPOINTS = {
    COURSES: {
        BASE: '/courses',
        GENERATE: '/courses/generate',
        DETAIL: (id: string) => `/courses/${id}`,
    },
    RUNNING: {
        START: '/running/start',
        UPDATE: (sessionId: string) => `/running/${sessionId}`,
        LOCATION: (sessionId: string) => `/running/${sessionId}/location`,
        FINISH: (sessionId: string) => `/running/${sessionId}/finish`,
    },
};
