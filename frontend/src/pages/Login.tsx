import React, { useState } from "react";
import { Link } from "react-router-dom";

interface Props {}

const Login: React.FC<Props> = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const { email, password } = formData;

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);

    // login(email, password);
  };

  // Is the user authenticated?
  // redirect to the home page

  return (
    <div className="container mt-5">
      <h1>Sign In</h1>
      <p>Sign in to your account</p>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <input
            type="email"
            className="form-control"
            placeholder="Email"
            name="email"
            value={email}
            onChange={onChange}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            className="form-control"
            placeholder="Password"
            name="password"
            value={password}
            onChange={onChange}
            minLength={6}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
      <p className="mt-3">
        Don't have an account? <Link to="/signup">Sign up</Link>
      </p>
      <p className="mt-3">
        Forgot your password? <Link to="/reset-password">Reset Password</Link>
      </p>
    </div>
  );
};

// const mapStateToProps = (state: any) => ({
//   isAuthenticated: state.auth.isAuthenticated,
// });

export default Login;
