import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import Navbar from "@/components/Navbar";
import Home from "@/pages/Home";
import Login from "@/pages/Login";
import Signup from "@/pages/Signup";
import Profile from "@/pages/Profile";
import Dashboard from "@/pages/Dashboard";
import Markets from "@/pages/Markets";
import CreateMarket from "@/pages/CreateMarket";
import Leaderboards from "@/pages/Leaderboards";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Navbar />
        <Routes>
          {/* <Route path='*' element={<NotFound />} /> */}

          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/markets" element={<Markets />} />
          <Route path="/markets/new" element={<CreateMarket />} />
          <Route path="/leaderboards" element={<Leaderboards />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
