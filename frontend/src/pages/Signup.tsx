import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as Yup from "yup";

interface Props {}

const Signup: React.FC<Props> = () => {
  const navigate = useNavigate();

  if (localStorage.getItem("token")) navigate("/");

  const formik = useFormik({
    initialValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
    validationSchema: Yup.object({
      username: Yup.string()
        .max(15, "Must be 15 characters or less")
        .required("Required"),
      email: Yup.string().email("Invalid email address").required("Required"),
      password: Yup.string()
        .min(6, "Must be at least 6 characters")
        .required("Required"),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref("password"), null], "Passwords must match")
        .required("Required"),
    }),
    onSubmit: (values) =>
      fetch("http://localhost:8000/api/auth/registration/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          Object.assign(values, {
            password1: values.password,
            password2: values.confirmPassword,
          })
        ),
      }).then(async (response) => {
        const data = await response.json();
        if (!response.ok) return Promise.reject(data);
        localStorage.setItem("token", data.key);
        navigate("/", { replace: true });
      }),
  });

  return (
    <div className="container mt-5">
      <h1>Sign up to create your new account!</h1>
      <form onSubmit={formik.handleSubmit}>
        <div className="container">
          <div className="row row-cols-1 row-cols-md-2">
            <div className="mb-3">
              <label htmlFor="username" className="form-label">
                Username
              </label>
              <input
                type="text"
                name="username"
                id="username"
                className={`form-control ${
                  formik.touched.username &&
                  formik.errors.username &&
                  "border-danger"
                }`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.username}
              />
              {formik.touched.username && formik.errors.username && (
                <div className="text-danger">{formik.errors.username}</div>
              )}
            </div>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">
                Email
              </label>
              <input
                type="email"
                name="email"
                id="email"
                className={`form-control ${
                  formik.touched.email && formik.errors.email && "border-danger"
                }`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.email}
              />
              {formik.touched.email && formik.errors.email && (
                <div className="text-danger">{formik.errors.email}</div>
              )}
            </div>
            <div className="mb-3">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                type="password"
                name="password"
                id="password"
                className={`form-control ${
                  formik.touched.password &&
                  formik.errors.password &&
                  "border-danger"
                }`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.password}
              />
              {formik.touched.password && formik.errors.password && (
                <div className="text-danger">{formik.errors.password}</div>
              )}
            </div>
            <div className="mb-3">
              <label htmlFor="confirmPassword" className="form-label">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                id="confirmPassword"
                className={`form-control ${
                  formik.touched.confirmPassword &&
                  formik.errors.confirmPassword &&
                  "border-danger"
                }`}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.confirmPassword}
              />
              {formik.touched.confirmPassword &&
                formik.errors.confirmPassword && (
                  <div className="text-danger">
                    {formik.errors.confirmPassword}
                  </div>
                )}
            </div>
          </div>
        </div>
        <button type="submit" className="btn btn-primary" disabled={formik.isSubmitting}>
          Sign Up
        </button>
      </form>
      <p className="mt-3">
        Already have an account? <Link to="/login">Sign In</Link>
      </p>
    </div>
  );
};

export default Signup;
