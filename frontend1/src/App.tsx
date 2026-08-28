import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import MainApp from "./pages/MainApp";
import RealtimeTest from "./RealtimeTest";
import SignupPage from "./pages/SignupPage";
import ProtectedRoute from "./ProtectedRoute";


function App() {
    return (
        <BrowserRouter>
            <Routes>

                <Route
                    path="/"
                    element={<LandingPage />}
                />

                <Route
                    path="/login"
                    element={<LoginPage />}
                />

                <Route
                    path="/app"
                    element={
                        <ProtectedRoute>
                            <MainApp />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/realtime-test"
                    element={<RealtimeTest />}
                />

                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/"
                            replace
                        />
                    }
                />

                <Route
                    path="/signup"
                    element={<SignupPage />}
                />

            </Routes>
        </BrowserRouter>
    );
}

export default App;