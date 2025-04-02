# Auth0 Integration Requirements

Please fill in the details below for your desired Auth0 integration.

## 1. Application Type

-   **Type:** [Specify: Regular Web App, Single Page App (SPA), Native App, Machine-to-Machine (M2M)]

## 2. Authentication Methods

Choose one or more methods:

-   [ ] Username/Password Database
-   [ ] Google Social Login
-   [ ] Facebook Social Login
-   [ ] GitHub Social Login
-   [ ] SAML
-   [ ] Other (Specify): __________

## 3. URLs

-   **Allowed Callback URLs:** [List comma-separated URLs, e.g., `http://localhost:3000/callback`, `https://myapp.com/callback`]
-   **Allowed Logout URLs:** [List comma-separated URLs, e.g., `http://localhost:3000`, `https://myapp.com`]
-   **Allowed Web Origins:** [List comma-separated URLs, e.g., `http://localhost:3000`]
-   **Allowed Origins (CORS):** [List comma-separated URLs, e.g., `http://localhost:3000`]

## 4. User Experience

-   **Login Redirect:** [Where should users be redirected after successful login? e.g., `/dashboard`]
-   **Logout Redirect:** [Where should users be redirected after logout? e.g., `/`]
-   **Custom Login Page:** [Do you need a custom login page experience (Universal Login customization)? Yes/No]
-   **Branding:** [Any specific branding requirements? Logo URL, colors, etc.]

## 5. Security

-   **Multi-Factor Authentication (MFA):** [Enforce MFA? Always / Adaptive / Never]
-   **Password Policy:** [Specify complexity requirements if using Database connection: Min Length, Character Types etc. Default is recommended.]

## 6. Roles & Permissions

-   **Enable Role-Based Access Control (RBAC):** [Yes/No]
-   **Define Roles:** [If Yes, list roles, e.g., `admin`, `editor`, `viewer`]
-   **Assign Permissions to Roles:** [If Yes, describe basic permission structure or provide details]

## 7. APIs

-   **Need to Secure an API:** [Yes/No]
-   **API Identifier (Audience):** [If Yes, specify the API audience]
-   **Scopes/Permissions:** [If Yes, list required API scopes/permissions]

## 8. Custom Data

-   **Custom Claims in Tokens:** [Need custom data added to ID or Access Tokens? Yes/No. If Yes, specify claims and source (e.g., user metadata)]
-   **User Metadata:** [Need to store custom data about users? Yes/No. If Yes, specify fields]

## 9. Migration

-   **Migrating Existing Users:** [Yes/No. If Yes, specify source (e.g., database, other provider)]

## 10. Other Notes

[Add any other specific requirements or context here]
