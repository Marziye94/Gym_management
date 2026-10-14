# Gym Management Application Flow

```mermaid
flowchart TD
    A([Program start]) --> D[Create shared repositories and services once]
    D --> S{Start menu: select role or Exit}
    S -->|Exit| E([Exit])
    S -->|Manager / Coach / Member| L[Enter username and password]
    L --> V{Active account and matching role?}
    V -->|No| F[Show login failure]
    F --> R{Retry or Back?}
    R -->|Retry| L
    R -->|Back| S
    V -->|Manager| M[Manager panel]
    V -->|Coach| C[Coach panel]
    V -->|Member| U[Member panel]
    M --> MU[User Management]
    M --> MH[Hall Management]
    M --> MC[Class Management]
    M --> MS[Subscription and Payment Management]
    M --> MR[Reports]
    MU -->|Back| M
    MH -->|Back| M
    MC -->|Back| M
    MS -->|Back| M
    MR -->|Back| M
    C --> CC[View My Classes]
    C --> CW[Manage Member Workout Plans]
    CC -->|Return| C
    CW -->|Select own class and enrolled Member| WP[View / Create Plan / Add / Edit Exercise]
    WP -->|Back| C
    U --> UP[Profile and Subscription Status]
    U --> UW[Wallet: Balance / Charge / Transactions / Subscription]
    U --> UC[Classes: Available / Register / My Registrations / Cancel]
    U --> UX[View Workout Plan]
    UP -->|Return| U
    UW -->|Back| U
    UC -->|Back| U
    UX -->|Return| U
    M -->|Logout| S
    C -->|Logout| S
    U -->|Logout| S
```

All feature menus receive the authenticated user and the same application dependencies.
Controlled feature file errors show a message and return to the parent panel.
Unavailable startup data disables the related features while other menus remain available.
Profile, class-list and workout-plan views return immediately after displaying their output.
The workout exercise menu returns to the Coach panel on Back, matching its current entry function.
