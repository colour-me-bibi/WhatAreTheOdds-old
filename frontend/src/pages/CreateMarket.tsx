import React from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Formik,
  Field,
  Form,
  ErrorMessage,
  FieldArray,
  FieldProps,
} from "formik";
import * as Yup from "yup";

import { Routes } from "@/api";

interface Props {}

const ContractSchema = Yup.object({
  name: Yup.string().max(32, "Must be 32 characters or less"),
  description: Yup.string().required("Description is required"),
});

const ContractNameDefaultValues = ["Latest Price", "", null, undefined];

const TagSchema = Yup.object({
  name: Yup.string().max(16, "Must be 16 characters or less").required(),
});

const MarketSchema = Yup.object({
  prompt: Yup.string().required("Prompt is required"),
  tags: Yup.array(TagSchema),
  projectedEnd: Yup.date().min(
    new Date(),
    "Projected end date must be in the future"
  ),
  contracts: Yup.array(ContractSchema)
    .required("At least one contract is required")
    .test(
      "defaultContract",
      "A sole contract must be blank or have the default name. When there's several contracts, none of them can be blank or have the default name.",
      (value) =>
        (value?.length === 1 &&
          ContractNameDefaultValues.includes(value[0].name)) ||
        ((value?.length ?? 0) > 1 &&
          value!.every((c) => !ContractNameDefaultValues.includes(c.name)))
    ),
});

const initialValues = {
  prompt: undefined,
  tags: [{ name: "" }],
  contracts: [
    {
      name: "Latest Price",
      description: undefined,
      projectedEnd: undefined,
    },
  ],
};

const CreateMarket: React.FC<Props> = () => {
  const navigate = useNavigate();

  if (localStorage.getItem("token")) {
    // TODO handle not logged in
  }

  return (
    <div className="container mt-5">
      <h1>Create a new market!</h1>
      <Formik
        initialValues={initialValues}
        validationSchema={MarketSchema}
        onSubmit={(values) =>
          Routes.create(Routes.Endpoint.markets, values).then((response) =>
            navigate(`/markets/${response.data.id}/`, { replace: true })
          )
        }
      >
        {({ values }) => (
          <Form>
            <Field name="prompt">
              {({ field, meta }: FieldProps) => (
                <div className="mb-3">
                  <label htmlFor="prompt" className="form-label">
                    Prompt
                  </label>
                  <input
                    {...field}
                    type="text"
                    id="prompt"
                    placeholder="Prompt"
                    className={`form-control ${
                      meta.touched && meta.error && "border-danger"
                    }`}
                  />
                </div>
              )}
            </Field>
            <ErrorMessage name="prompt" />
            <FieldArray name="tags">
              {({ push, remove }) => (
                <div>
                  {values.tags.map((tag, index) => (
                    <div key={index}>
                      <Field name={`tags[${index}].name`}>
                        {({ field, meta }: FieldProps) => (
                          <div className="mb-3">
                            <label
                              htmlFor={`tags[${index}].name`}
                              className="form-label"
                            >
                              Tag
                            </label>
                            <input
                              {...field}
                              type="text"
                              id={`tags[${index}].name`}
                              placeholder="Tag"
                              className={`form-control ${
                                meta.touched && meta.error && "border-danger"
                              }`}
                            />
                          </div>
                        )}
                      </Field>
                      <ErrorMessage name={`tags[${index}].name`} />
                      <button type="button" onClick={() => remove(index)}>
                        Remove
                      </button>
                    </div>
                  ))}
                  <button type="button" onClick={() => push({})}>
                    Add tag
                  </button>
                </div>
              )}
            </FieldArray>
            <Field name="projectedEnd">
              {({ field, meta }: FieldProps) => (
                <div className="mb-3">
                  <label htmlFor="projectedEnd" className="form-label">
                    Projected end date
                  </label>
                  <input
                    {...field}
                    type="date"
                    id="projectedEnd"
                    placeholder="Projected end date"
                    className={`form-control ${
                      meta.touched && meta.error && "border-danger"
                    }`}
                  />
                </div>
              )}
            </Field>
            <ErrorMessage name="projectedEnd" />
            <FieldArray name="contracts">
              {({ push, remove }) => (
                <div>
                  {values.contracts.map((contract, index) => (
                    <div key={index}>
                      <Field name={`contracts[${index}].name`}>
                        {({ field, meta }: FieldProps) => (
                          <div className="mb-3">
                            <label
                              htmlFor={`contracts[${index}].name`}
                              className="form-label"
                            >
                              Contract {index}
                            </label>
                            <input
                              {...field}
                              type="text"
                              id={`contracts[${index}].name`}
                              placeholder="Name"
                              className={`form-control ${
                                meta.touched && meta.error && "border-danger"
                              }`}
                            />
                          </div>
                        )}
                      </Field>
                      <ErrorMessage name={`contracts[${index}].name`} />
                      <Field name={`contracts[${index}].description`}>
                        {({ field, meta }: FieldProps) => (
                          <div className="mb-3">
                            <label
                              htmlFor={`contracts[${index}].description`}
                              className="form-label"
                            >
                              Description
                            </label>
                            <textarea
                              {...field}
                              id={`contracts[${index}].description`}
                              placeholder="Description"
                              className={`form-control ${
                                meta.touched && meta.error && "border-danger"
                              }`}
                            />
                          </div>
                        )}
                      </Field>
                      <ErrorMessage name={`contracts[${index}].description`} />
                      <Field name={`contracts[${index}].projectedEnd`}>
                        {({ field, meta }: FieldProps) => (
                          <div className="mb-3">
                            <label
                              htmlFor={`contracts[${index}].projectedEnd`}
                              className="form-label"
                            >
                              Projected end date
                            </label>
                            <input
                              {...field}
                              type="date"
                              id={`contracts[${index}].projectedEnd`}
                              placeholder="Projected end date"
                              className={`form-control ${
                                meta.touched && meta.error && "border-danger"
                              }`}
                            />
                          </div>
                        )}
                      </Field>
                      <ErrorMessage name={`contracts[${index}].projectedEnd`} />
                      <button type="button" onClick={() => remove(index)}>
                        Remove
                      </button>
                    </div>
                  ))}
                  <button type="button" onClick={() => push({})}>
                    Add contract
                  </button>
                </div>
              )}
            </FieldArray>
            <button type="submit">Submit</button>

            <Link to="/">Cancel</Link>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default CreateMarket;
