# BVMS Frontend Onboarding Guide

> A comprehensive guide for new developers joining the BBC Chartering Vessel Management System (BVMS) frontend project. Read this before writing any code.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Tech Stack](#2-tech-stack)
3. [Code Guidelines](#3-code-guidelines)
4. [Reusable Components](#4-reusable-components-library)
5. [Complex Feature Example](#5-complex-feature-walkthrough)
6. [Discussion & Improvement Suggestions](#6-discussion--improvement-suggestions)

---

## 1. Project Structure

### High-Level Architecture

This project uses a **hybrid architecture**: feature-based organization for domain logic + a shared layer for common utilities and UI components.

```
bbc-bvms-net-react-codebase/
├── app/                    # Next.js App Router (pages & routing)
│   ├── layout.tsx          # Root layout (providers wrap here)
│   ├── (dashboard)/        # Authenticated routes (main app)
│   │   ├── estimate/       # Voyage estimation module
│   │   ├── voyage/         # Voyage management
│   │   ├── shipment/       # Shipment management
│   │   ├── vessel/         # Vessel management
│   │   ├── masterdata/     # Master data admin
│   │   └── ...             # (20+ other modules)
│   ├── (noauth)/           # Unauthenticated routes (login)
│   ├── (backend)/          # API routes (server-side)
│   └── (loading)/          # Loading states
│
├── features/               # 🔑 CORE: Domain features (business logic)
│   ├── common/             # Shared across all features
│   ├── estimate/           # Voyage estimate feature
│   ├── voyage/             # Voyage feature
│   ├── shipment/           # Shipment feature
│   ├── invoice/            # Invoice feature
│   └── ...                 # (25+ feature modules)
│
├── components/             # Shared UI components (Atomic Design)
│   ├── atoms/              # Basic building blocks (inputs, buttons, modals)
│   └── desktop/            # Desktop layout wrapper & toolbar
│
├── core/                   # Framework-level shared code
│   ├── hooks/              # Global custom hooks
│   ├── utils/              # Global utility functions
│   ├── HOC/                # Higher-order components
│   └── storage/            # Local storage helpers
│
├── config/                 # Global constants & configuration
├── http/                   # 🔑 Auto-generated API clients
│   ├── app/                # Application backend (DTOs + Services)
│   └── master/             # Master data backend (DTOs + Services)
│
├── lib/                    # Pre-configured libraries
│   ├── client/             # OpenAPI fetch + React Query clients
│   ├── msal-auth/          # Azure MSAL authentication
│   ├── next-auth/          # NextAuth configuration
│   └── axiosSetup.ts       # Legacy Axios interceptors
│
├── layout/                 # Layout providers
│   ├── AuthProvider/       # MSAL + NextAuth auth flow
│   └── GlobalProvider/     # Ant Design, React Query, NuqsAdapter, etc.
│
├── types/                  # Global TypeScript types
├── assets/                 # Static assets (icons, SVGs, JSON)
├── test/                   # Test utilities and mocks
├── e2e/                    # Playwright E2E tests
└── docs/                   # Documentation (you are here)
```

### Feature Folder Convention

Every feature follows the same internal structure. When you create a new feature, replicate this pattern:

```
features/<feature-name>/
├── api/                    # React Query hooks for data fetching
│   ├── useFeatureAPI.ts    # Query hooks (GET)
│   └── useFeatureMutation.ts # Mutation hooks (POST, PUT, DELETE)
├── components/             # Feature-specific UI components
├── constants/              # Feature-specific constants & enums
├── helpers/                # Pure functions for business logic
├── hooks/                  # Feature-specific custom hooks
├── pages/                  # Page-level components (composed from smaller ones)
├── store/                  # Zustand stores (if needed)
├── utils/                  # Feature-specific utilities
├── schemas/                # Zod validation schemas (if applicable)
├── context/                # React Context providers (if needed)
├── modal/                  # Modal components (if applicable)
└── index.ts                # Public API — export only what others need
```

### Path Aliases

The project configures these path aliases in `tsconfig.json`:

| Alias           | Maps To                       | Usage                                            |
| --------------- | ----------------------------- | ------------------------------------------------ |
| `@/*`           | `./*`                         | General imports: `@/components/...`, `@/lib/...` |
| `@components/*` | `./components/*`              | Atom components: `@components/atoms/a-input`     |
| `@features/*`   | `./features/*`                | Feature imports: `@features/common/types`        |
| `@helpers/*`    | `./features/common/helpers/*` | Shared helpers                                   |
| `@utils/*`      | `./features/common/utils/*`   | Shared utilities                                 |
| `@types/*`      | `./features/common/types/*`   | Shared types                                     |
| `@hooks/*`      | `./features/common/hooks/*`   | Shared hooks                                     |
| `@store/*`      | `./features/common/store/*`   | Shared stores                                    |
| `@styles/*`     | `./features/common/styles/*`  | Shared styles                                    |

### Routing Convention

This project uses the **Next.js App Router**. Key patterns:

- **Route Groups** `(dashboard)`, `(noauth)` — Organize routes without affecting the URL path
- **Dynamic Routes** `[id]` — Parameterized pages like `/estimate/voy/[id]`
- **Layouts** `layout.tsx` — Wraps child routes with providers, auth checks, and UI chrome
- **Pages** `page.tsx` — The route's rendered content

**Example: Estimate detail page**

```
app/(dashboard)/estimate/voy/[id]/page.tsx  →  URL: /estimate/voy/:id
```

The page component is thin — it extracts route params, initializes data, and renders the feature component:

```tsx
'use client';
import { useParams } from 'next/navigation';
import { Estimate } from '@/features/estimate';
import { useInitializeEstimateDetailFromEstimate } from '@/features/estimate/hooks/useInitializeEstimateDetail';

export default function EstimateVoyagesDetail() {
  const params = useParams<{ id: string }>();
  const { isLoading } = useInitializeEstimateDetailFromEstimate(params?.id);

  return (
    <>
      {isLoading && <LoadingWrapper isLoading />}
      <div style={{ display: isLoading ? 'none' : 'block' }}>
        <Estimate />
      </div>
    </>
  );
}
```

---

## 2. Tech Stack

### Core Framework

| Technology     | Version | Purpose                                         |
| -------------- | ------- | ----------------------------------------------- |
| **Next.js**    | 16.x    | React framework with App Router, SSR, Turbopack |
| **React**      | 19.x    | UI library (with React Compiler enabled)        |
| **TypeScript** | 5.x     | Type safety                                     |

### State Management

| Technology                       | Purpose                       | When to Use                                                   |
| -------------------------------- | ----------------------------- | ------------------------------------------------------------- |
| **Zustand**                      | Client-side application state | Complex cross-component state (estimate editor, worksheet)    |
| **React Query (TanStack Query)** | Server state / data fetching  | ALL API data (queries + mutations)                            |
| **React Hook Form**              | Form state                    | Multi-field forms with validation                             |
| **nuqs**                         | URL query parameters state    | Bookmarkable/shareable UI state (filters, selected tabs, IDs) |
| **React `useState`**             | Local component state         | Simple UI toggles, temporary values                           |

### UI & Styling

| Technology                | Purpose                                                 |
| ------------------------- | ------------------------------------------------------- |
| **Ant Design (antd)**     | Primary component library (tables, forms, modals, etc.) |
| **Tailwind CSS**          | Utility-first CSS for custom styling                    |
| **SCSS Modules**          | Scoped styles for complex components                    |
| **AG Grid**               | Enterprise data grid for large tables                   |
| **clsx / tailwind-merge** | Conditional class name composition                      |
| **Framer Motion**         | Animations                                              |
| **Mapbox GL**             | Map visualization                                       |

### Data & API

| Technology              | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| **openapi-fetch**       | Type-safe HTTP client generated from OpenAPI specs |
| **openapi-react-query** | React Query integration for openapi-fetch          |
| **Axios**               | Legacy HTTP client (being migrated away)           |
| **Zod**                 | Schema validation                                  |
| **SignalR**             | Real-time WebSocket communication                  |

### Auth & Security

| Technology               | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| **Azure MSAL**           | Microsoft Entra ID (Azure AD) authentication |
| **NextAuth v5**          | Session management + credential provider     |
| **Application Insights** | Telemetry & monitoring                       |

### Dev Tooling

| Tool                       | Purpose                  |
| -------------------------- | ------------------------ |
| **Yarn 4**                 | Package manager (PnP)    |
| **Turbopack**              | Fast dev server & builds |
| **ESLint**                 | Code linting             |
| **Prettier**               | Code formatting          |
| **Husky + lint-staged**    | Pre-commit hooks         |
| **Jest + Testing Library** | Unit & integration tests |
| **Playwright**             | End-to-end tests         |
| **React DevTools**         | Component debugging      |
| **React Query DevTools**   | Query state inspection   |

### Running the Project

```bash
# Install dependencies
yarn install

# Start dev server (port 3333)
yarn dev

# Build for production
yarn build

# Run tests
yarn test

# Run E2E tests
yarn e2e
```

---

## 3. Code Guidelines

### 3.1 State Management: What to Use When

This is the **most important decision** you'll make for each feature. Follow this decision tree:

```
Is the data coming from the backend API?
├── YES → Use React Query (useAppQuery / useMasterQuery)
│   └── Need to transform or share that data across many components?
│       ├── Use the `select` option in the query hook
│       └── OR put derived state in a Zustand store
│
└── NO → It's client-side state
    ├── Is it a form with multiple fields?
    │   └── YES → Use React Hook Form (useForm / useFormContext)
    │
    ├── Is it a simple toggle, visibility, or local value?
    │   └── YES → Use React useState
    │
    ├── Should it survive in the URL (shareable, bookmarkable)?
    │   └── YES → Use nuqs (useQueryState)
    │
    └── Is it complex state shared across many components in a feature?
        └── YES → Use Zustand store
```

#### React Query (Server State) — The Default for API Data

```tsx
// ✅ CORRECT: Use the typed query hooks
import { useAppQuery } from '@/lib/client/app.client';

const { data, isLoading, error } = useAppQuery(
  'get',
  '/Estimates/{estimateId}',
  {
    params: { path: { estimateId: id } },
  },
  {
    enabled: !!id, // only fetch when ID exists
    select: (response) => response.result, // transform the response
  }
);
```

```tsx
// ✅ CORRECT: Mutation with lifecycle hooks
import { useAppMutation } from '@/lib/client/app.client';

const mutation = useAppMutation('post', '/Estimates', {
  onSuccess: (data) => {
    showSuccess('Estimate created');
    queryClient.invalidateQueries({ queryKey: ['estimates'] });
  },
  onError: () => showError('Failed to create estimate'),
});

// Call it
mutation.mutate({ body: estimateData });
```

#### Zustand Store (Complex Client State)

```tsx
// store.tsx — Define types, state, actions separately
import { createStore } from 'zustand/vanilla';
import { devtools } from 'zustand/middleware';
import { produce } from 'immer';

type State = {
  selectedItemId: string | null;
  filters: FilterConfig;
};

type Actions = {
  setSelectedItem: (id: string | null) => void;
  updateFilters: (filters: Partial<FilterConfig>) => void;
  resetState: () => void;
};

const defaultState: State = {
  selectedItemId: null,
  filters: {},
};

export const createMyStore = (initState = defaultState) =>
  createStore<State & Actions>()(
    devtools((set) => ({
      ...initState,

      setSelectedItem: (id) => set({ selectedItemId: id }),

      // Use immer's produce() for complex nested updates
      updateFilters: (filters) =>
        set(
          produce((draft) => {
            draft.filters = { ...draft.filters, ...filters };
          })
        ),

      resetState: () => set(defaultState),
    }))
  );
```

**Providing the store via layout:**

```tsx
// app/(dashboard)/myfeature/layout.tsx
import { MyFeatureStoreProvider } from './store';

export default function Layout({ children }) {
  return <MyFeatureStoreProvider>{children}</MyFeatureStoreProvider>;
}
```

#### nuqs (URL State)

```tsx
import { useQueryState } from 'nuqs';

// State synced to URL: ?tab=details
const [activeTab, setActiveTab] = useQueryState('tab', { defaultValue: 'overview' });
```

#### React Hook Form

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  vesselName: z.string().min(1, 'Required'),
  speed: z.number().positive(),
});

const {
  register,
  handleSubmit,
  formState: { errors },
} = useForm({
  resolver: zodResolver(schema),
});
```

### 3.2 Where to Put Code

| What You're Writing                               | Where to Put It                                                     |
| ------------------------------------------------- | ------------------------------------------------------------------- |
| A new page/route                                  | `app/(dashboard)/<module>/page.tsx`                                 |
| A feature component                               | `features/<feature>/components/`                                    |
| A feature API hook                                | `features/<feature>/api/`                                           |
| A feature custom hook                             | `features/<feature>/hooks/`                                         |
| Business logic (pure functions)                   | `features/<feature>/helpers/`                                       |
| Feature-specific constants/enums                  | `features/<feature>/constants/`                                     |
| Feature-level Zustand store                       | `features/<feature>/store/` or `app/(dashboard)/<module>/store.tsx` |
| A **reusable** UI component (used by 2+ features) | `components/atoms/` or `features/common/components/`                |
| A **reusable** hook (used by 2+ features)         | `core/hooks/` or `features/common/hooks/`                           |
| A **reusable** utility function                   | `core/utils/` or `features/common/helpers/`                         |
| A shared API hook (currencies, users, ports)      | `features/common/api/`                                              |
| A reusable select dropdown                        | `features/common/components/select/Select<Name>.tsx`                |
| Global constants                                  | `config/`                                                           |
| TypeScript types shared across features           | `types/` or `features/common/types/`                                |
| Test files                                        | Co-locate as `__tests__/` folder next to the source                 |

**Key Rule:** Feature-specific code stays inside the feature folder. Only promote to `common/` or `core/` when 2+ features need it.

### 3.3 Component Design: Stateless vs Stateful

#### Stateless (Presentation) Components — Preferred

Most components should be **stateless**. They receive data via props and emit events up:

```tsx
// ✅ Stateless - Pure presentation
interface ShipmentRowProps {
  shipment: ShipmentDto;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

function ShipmentRow({ shipment, onSelect, isSelected }: ShipmentRowProps) {
  return (
    <tr className={isSelected ? 'bg-blue-50' : ''} onClick={() => onSelect(shipment.id)}>
      <td>{shipment.name}</td>
      <td>{shipment.status}</td>
    </tr>
  );
}
```

#### Stateful (Container) Components — Use Sparingly

Stateful components own data and orchestrate child components. Typically these are **page-level** or **section-level** components:

```tsx
// Stateful - Manages data and coordinates children
function ShipmentList() {
  const { data: shipments, isLoading } = useAppQuery('get', '/Shipments', ...);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  if (isLoading) return <LoadingWrapper isLoading />;

  return (
    <table>
      {shipments.map((s) => (
        <ShipmentRow
          key={s.id}
          shipment={s}
          isSelected={s.id === selectedId}
          onSelect={setSelectedId}
        />
      ))}
    </table>
  );
}
```

#### Design Rules

1. **Keep components small** — Under 200 lines ideally, 400 max
2. **Lift state up** — If two siblings need the same data, lift state to the parent
3. **Render props or composition** — Prefer composition over deeply nested prop drilling
4. **Use the Context Factory** for feature-scoped state instead of prop-drilling through 4+ levels:

```tsx
import { createContextFactory } from '@/core/utils/create-context-factory';

const [MyProvider, useMyStore] = createContextFactory<MyState>('MyFeature');

// In parent:
<MyProvider value={stateData}>{children}</MyProvider>;

// In deeply nested child:
const value = useMyStore((s) => s.someField);
```

### 3.4 Interacting with Backend APIs

The project has **two backends** with auto-generated, type-safe clients:

| Backend                         | Client File                   | Hooks                                 | Types          |
| ------------------------------- | ----------------------------- | ------------------------------------- | -------------- |
| **App API** (business logic)    | `lib/client/app.client.ts`    | `useAppQuery`, `useAppMutation`       | `http/app/`    |
| **Master API** (reference data) | `lib/client/master.client.ts` | `useMasterQuery`, `useMasterMutation` | `http/master/` |

#### How Auto-Generation Works

```bash
# Regenerate from Swagger (DON'T manually edit http/ files)
yarn gen:api:app      # Generates http/app/ types from App backend swagger
yarn gen:api:master   # Generates http/master/ types from Master backend swagger
```

The generated types in `http/app/models/` (500+ DTOs) and `http/master/models/` (300+ DTOs) give you full type-safety for API requests and responses.

#### Writing a Query Hook (Recommended Pattern)

Create a file in `features/<feature>/api/`:

```tsx
// features/myfeature/api/useMyFeatureAPI.ts
import { useAppQuery } from '@/lib/client/app.client';

// 1. Define query keys for cache management
export const myFeatureKeys = {
  list: ['myfeature', 'list'] as const,
  detail: (id: string) => ['myfeature', id] as const,
};

// 2. Export named hooks
export const useGetMyFeatureList = (filters?: FilterParams) => {
  return useAppQuery(
    'get',
    '/MyFeature',
    {
      params: { query: filters },
    },
    {
      enabled: true,
      select: (data) => data.result ?? [],
    }
  );
};

export const useGetMyFeatureDetail = (id: string | null) => {
  return useAppQuery(
    'get',
    '/MyFeature/{id}',
    {
      params: { path: { id: id! } },
    },
    {
      enabled: !!id,
      select: (data) => data.result,
    }
  );
};
```

#### Writing a Mutation Hook

```tsx
// features/myfeature/api/useMyFeatureMutation.ts
import { useAppMutation } from '@/lib/client/app.client';
import { useQueryClient } from '@tanstack/react-query';
import { useNotification } from '@/core/hooks/useNotification';

export const useCreateMyFeature = () => {
  const queryClient = useQueryClient();
  const { showSuccess, showError } = useNotification();

  return useAppMutation('post', '/MyFeature', {
    onSuccess: () => {
      showSuccess('Created successfully');
      queryClient.invalidateQueries({ queryKey: ['myfeature'] });
    },
    onError: () => showError('Failed to create'),
  });
};
```

#### Legacy Pattern (Avoid for New Code)

Some older features use `axios` + manually defined service classes. If you encounter this pattern, prefer the `useAppQuery`/`useAppMutation` approach for new code:

```tsx
// ❌ LEGACY — don't write new code like this
import { EstimatesService } from '@/http/app';
const result = await EstimatesService.getEstimate(id);

// ✅ MODERN — use typed query hooks
const { data } = useAppQuery('get', '/Estimates/{id}', { params: { path: { id } } });
```

### 3.5 Data Workflow & Component Communication

#### Pattern 1: Parent → Child (Props)

The most common pattern. Parent fetches data, passes it down:

```
PageComponent (fetches data via useAppQuery)
  └── SectionComponent (receives data as prop)
       ├── TableComponent (receives rows as prop)
       │    └── RowComponent (receives single item as prop)
       └── FormComponent (receives initial values as prop)
```

#### Pattern 2: Child → Parent (Callback Props)

Child components notify parents via callback functions:

```tsx
// Parent
function ShipmentPage() {
  const handleSave = (updatedItems: ProfitAndLossItemDto[]) => {
    mutation.mutate(updatedItems);
  };

  return <ProfitAndLossItemsTable items={items} onSave={handleSave} />;
}

// Child emits changes upward
function ProfitAndLossItemsTable({ items, onSave }: Props) {
  const handleOnSave = (updatedItem) => {
    const newItems = [...items];
    // ... update logic
    onSave(newItems); // Notify parent
  };
}
```

#### Pattern 3: Shared Store (Zustand — for Complex Features)

When multiple components in a feature need to read/write the same state:

```
Layout (provides store via context)
  └── Page
       ├── Sidebar (reads store.selectedItem, calls store.setSelectedItem)
       ├── Editor (reads store.estimate, calls store.updateEstimate)
       └── Toolbar (reads store.status, calls store.resetEstimate)
```

```tsx
// Any component in the tree:
import { useEstimateStore } from '../store';

function Editor() {
  const estimate = useEstimateStore((s) => s.estimate);
  const updateEstimate = useEstimateStore((s) => s.updateEstimate);

  return <input value={estimate.name} onChange={(e) => updateEstimate({ name: e.target.value })} />;
}
```

#### Pattern 4: URL State (Shareable State)

For state that should be bookmarkable or persist across navigation:

```tsx
// Component A writes to URL
const [selectedTab, setSelectedTab] = useQueryState('tab');
setSelectedTab('cargo');

// Component B reads the same URL param
const [selectedTab] = useQueryState('tab');
// selectedTab === 'cargo'
```

#### Pattern 5: Real-Time Updates (SignalR)

For live data from the server:

```tsx
import { useSignalR } from '@/core/hooks/useSignalR';

useSignalR('EntityUpdated', (payload) => {
  queryClient.invalidateQueries({ queryKey: ['estimates', payload.id] });
});
```

### 3.6 Immutability Rules

**CRITICAL:** Never mutate state directly. Always create new objects.

```tsx
// ❌ WRONG — mutation
items[index] = updatedItem;
setItems(items);

// ✅ CORRECT — immutable update
const newItems = [...items];
newItems[index] = { ...newItems[index], ...updatedItem };
setItems(newItems);

// ✅ ALSO CORRECT — use immer inside Zustand
set(
  produce((draft) => {
    draft.items[index] = { ...draft.items[index], ...updatedItem };
  })
);
```

### 3.7 Error Handling

```tsx
// API errors
const { showError } = useNotification();

try {
  await mutation.mutateAsync(data);
} catch (error) {
  showError('Operation failed. Please try again.');
}

// Or use mutation callbacks (preferred)
useAppMutation('post', '/Endpoint', {
  onError: (error) => showError('Something went wrong'),
});
```

### 3.8 File Naming Conventions

| Type          | Convention                    | Example                         |
| ------------- | ----------------------------- | ------------------------------- |
| Components    | PascalCase                    | `ShipmentTable.tsx`             |
| Hooks         | camelCase with `use` prefix   | `useShipmentData.ts`            |
| Helpers/Utils | camelCase                     | `calculateFreight.ts`           |
| Constants     | camelCase with suffix         | `shipment.constant.ts`          |
| Stores        | camelCase                     | `store.ts` or `store.tsx`       |
| Types         | camelCase                     | `types.ts`                      |
| Styles        | kebab-case with module suffix | `table.module.scss`             |
| Tests         | Same name + test folder       | `__tests__/useShipment.test.ts` |

---

## 4. Reusable Components Library

### 4.1 Atom Components (`components/atoms/`)

These are the **base building blocks** wrapping Ant Design with project-wide defaults. **Always use these instead of raw `antd` components.**

| Component        | Import                                | Purpose                                             |
| ---------------- | ------------------------------------- | --------------------------------------------------- |
| `AInput`         | `@/components/atoms/a-input`          | Text input with `isLabelOnly` mode                  |
| `AInputNumber`   | `@/components/atoms/a-input-number`   | Number input with decimal control, negative support |
| `AButton`        | `@/components/atoms/a-button`         | Styled button                                       |
| `AModal`         | `@/components/atoms/a-modal`          | Modal dialog                                        |
| `ATooltip`       | `@/components/atoms/a-tooltip`        | Tooltip wrapper                                     |
| `ADatePicker`    | `@/components/atoms/a-date-picker`    | Date picker with dayjs                              |
| `ARangePicker`   | `@/components/atoms/a-range-picker`   | Date range picker                                   |
| `ATimePicker`    | `@/components/atoms/a-time-picker`    | Time picker                                         |
| `ATextarea`      | `@/components/atoms/a-textarea`       | Multi-line text input                               |
| `ACheckbox`      | `@/components/atoms/a-checkbox`       | Checkbox                                            |
| `ASwitch`        | `@/components/atoms/a-switch`         | Toggle switch                                       |
| `ATag`           | `@/components/atoms/a-tag`            | Tag/badge                                           |
| `ACard`          | `@/components/atoms/a-card`           | Card container                                      |
| `ASkeleton`      | `@/components/atoms/a-skeleton`       | Loading skeleton                                    |
| `AUpload`        | `@/components/atoms/a-upload`         | File upload                                         |
| `ADropdown`      | `@/components/atoms/a-dropdown`       | Dropdown menu                                       |
| `ACurrencyInput` | `@/components/atoms/a-currency-input` | Currency-specific number input                      |
| `Select`         | `@/components/atoms/select/select`    | Base select dropdown                                |
| `DataTable`      | `@/components/atoms/table`            | Ant Design table wrapper                            |
| `Collapsible`    | `@/components/atoms/collapsible`      | Collapsible section                                 |

**Key feature:** Most atom inputs support an `isLabelOnly` prop — when `true`, the input renders as plain text (read-only display mode). This is used throughout for toggling edit/view modes.

**Usage Example:**

```tsx
import { AInputNumber } from '@/components/atoms/a-input-number';

<AInputNumber
  value={record.totalValue}
  onChange={(value) => updateRow(index, { totalValue: value })}
  disabled={isReadOnly}
  isLabelOnly={isViewMode} // Renders as text when true
  decimals={2} // Decimal precision
  allowNegative={false} // Prevent negatives
  defaultValue={0}
/>;
```

### 4.2 Domain Select Components (`features/common/components/select/`)

The project has **100+ pre-built select dropdowns** for every domain entity. These handle data fetching, searching, and display internally.

| Select Component                          | What It Fetches               |
| ----------------------------------------- | ----------------------------- |
| `SelectVessel`                            | Vessels from master data      |
| `SelectPort`                              | Ports with search             |
| `SelectCurrency` / `SelectCurrencyId`     | Currency codes                |
| `SelectCounterParty`                      | Business partners             |
| `SelectBusinessPartner`                   | Business partners (alternate) |
| `SelectCargoType`                         | Cargo types                   |
| `SelectBunkerTypes`                       | Bunker fuel types             |
| `SelectTradeArea`                         | Trade areas                   |
| `SelectEstimate`                          | Voyage estimates              |
| `SelectVoyage`                            | Voyages                       |
| `SelectShipment`                          | Shipments                     |
| `SelectInvoiceItemType`                   | Invoice item types            |
| `SelectUser` / `SelectUserByRole`         | Users                         |
| `SelectCountryName` / `SelectCountryCode` | Countries                     |
| `SelectPaymentTerm`                       | Payment terms                 |
| `SelectOffice`                            | Office locations              |
| `SelectRole`                              | User roles                    |
| ...                                       | (80+ more)                    |

**Usage:** They all follow a consistent API:

```tsx
import { SelectPort } from '@/features/common/components/select';

<SelectPort
  value={selectedPortId}
  onChange={(portId) => handlePortChange(portId)}
  disabled={isReadOnly}
  allowClear
  className="!h-[24px] w-full"
  popupMatchSelectWidth={false} // Dropdown can be wider than trigger
  isLabelOnly={isViewMode} // Read-only text display
/>;
```

### 4.3 The `ApiSelect` Generic Component

For custom entity dropdowns not covered by pre-built selects:

```tsx
import ApiSelect from '@/features/common/components/select/ApiSelect';

<ApiSelect
  setting={{
    labelField: 'name',
    valueField: 'id',
    searchField: 'name',
  }}
  queryFn={MyService.getAll}
  value={selectedId}
  onChange={handleChange}
/>;
```

### 4.4 Common Utility Components

| Component             | Import From                                      | Purpose                                 |
| --------------------- | ------------------------------------------------ | --------------------------------------- |
| `LoadingWrapper`      | `@/features/common`                              | Wraps content with a loading spinner    |
| `FullScreenLoading`   | `@/features/common/components/FullScreenLoading` | Full-screen loading overlay             |
| `EmptyData`           | `@/features/common/components/EmptyData`         | Empty state placeholder                 |
| `ErrorFallback`       | `@/features/common/components/ErrorFallback`     | Error boundary fallback                 |
| `FeatureFlag`         | `@/features/common/components/FeatureFlag`       | Conditional feature rendering           |
| `StatusIndicator`     | `@/features/common/components/StatusIndicator`   | Status badge/indicator                  |
| `ButtonLink`          | `@/features/common/components/button/ButtonLink` | Navigation link styled as button        |
| `SplitViewForm`       | `@/features/common/components/SplitViewForm`     | Split-panel layout for forms            |
| `NewCellActions`      | `@features/estimate/components/estimate`         | Duplicate/Remove actions for table rows |
| `ShipmentTableFooter` | `@features/estimate/components/estimate`         | "Add New" row footer for tables         |
| `NavigationEvents`    | `@/features/common/components/NavigationEvent`   | Route change detection                  |
| `TelePortal`          | `@/features/common/components/TelePortal`        | React Portal helper                     |

### 4.5 Shared Custom Hooks

| Hook                        | Import                               | Purpose                           |
| --------------------------- | ------------------------------------ | --------------------------------- |
| `useNotification()`         | `@/core/hooks/useNotification`       | Show success/error/info toasts    |
| `useDebounce(value, delay)` | `@/core/hooks/useDebounce`           | Debounce any value                |
| `useDisclosure()`           | `@/core/hooks/useDisclosure`         | `{ isOpen, open, close, toggle }` |
| `useAppModal()`             | `@/core/hooks/useAppModal`           | Modal state management            |
| `useClickOutside(ref)`      | `@/core/hooks/useClickOutside`       | Click outside detection           |
| `useMounted()`              | `@/core/hooks/useMounted`            | Check if component is mounted     |
| `useSignalR()`              | `@/core/hooks/useSignalR`            | WebSocket real-time events        |
| `useCurrentUser()`          | `@/core/hooks/useCurrentUser`        | Current authenticated user info   |
| `useChangeSearchParams()`   | `@/core/hooks/useChangeSearchParams` | URL query param mutations         |
| `useCheckPermission()`      | `@hooks/useCheckPermission`          | RBAC permission checking          |
| `useFeatureFlags()`         | `@hooks/useFeatureFlags`             | Feature flag evaluation           |
| `useFormDirty()`            | `@hooks/useFormDirty`                | Track unsaved form changes        |
| `useUnsavedForm()`          | `@hooks/useUnsavedForm`              | Warn on unsaved navigation        |
| `useCurrency()`             | `@hooks/useCurrency`                 | Currency data & formatting        |
| `usePageTitle()`            | `@hooks/usePageTitle`                | Set browser tab title             |

---

## 5. Complex Feature Walkthrough

### ProfitAndLossItemsTable — Anatomy of a Complex Component

The `ProfitAndLossItemsTable` (attached file) is a representative example of a complex, real-world component. Let's break down the patterns it uses:

#### Data Flow Diagram

```
Parent Component (Shipment Page or Estimate Page)
│
├── Passes Down (Props):
│   ├── items: ProfitAndLossItemDto[]        ← The data
│   ├── onSave: (items) => void              ← Save callback
│   ├── onDirty: (items) => void             ← Dirty state callback
│   ├── onRemove: (id) => void               ← Delete callback
│   ├── shipment / estimate                  ← Context data
│   ├── restrictions                         ← Business constraints
│   ├── disabled / isLabelOnly               ← UI mode flags
│   └── hide*Column flags                    ← Column visibility
│
└── ProfitAndLossItemsTable
    │
    ├── Local State (useState):
    │   ├── items                             ← Filtered working copy
    │   ├── typeOptions                       ← Dropdown options
    │   ├── openPopupRestrictionValue         ← Modal visibility
    │   └── selectedRestriction               ← Currently editing restriction
    │
    ├── Custom Hook:
    │   └── useMiscExpensePortCount()         ← Port-count billing logic
    │
    ├── Handles Events:
    │   ├── addNewRow() → generates ID, creates default item → onSave()
    │   ├── updateRow() → merges changes → recalculates → onSave()
    │   ├── deleteRow() → filters out item → onSave()
    │   ├── duplicateRow() → clones with new ID → onSave()
    │   └── handlePaymentBasicSelection() → billing type logic → onSave()
    │
    └── Renders:
        ├── DataTable (antd table wrapper)
        │   ├── Columns with inline editable cells
        │   │   ├── SelectInvoiceItemType (domain dropdown)
        │   │   ├── SelectCounterParty (domain dropdown)
        │   │   ├── AInput (text input)
        │   │   ├── AInputNumber (number with decimals)
        │   │   ├── SelectCurrency (currency dropdown)
        │   │   ├── Select (generic dropdown)
        │   │   └── NewCellActions (duplicate/delete buttons)
        │   └── Footer: ShipmentTableFooter (add new button)
        │
        └── AModal (restriction value editor popup)
```

#### Key Patterns to Notice

**1. Props-heavy API with `hide*` flags for column visibility:**

```tsx
interface ProfitAndLossItemsTableProps {
  hideTypeColumn?: boolean;
  hideCounterPartyColumn?: boolean;
  hidePaymentBasisColumn?: boolean;
  // ... 10+ visibility flags
}
```

This pattern allows the same component to be reused across Estimate, Shipment, and Voyage pages with different column configurations.

**2. Inline editable table cells:**
Each column's `render` function returns an editable atom component that calls `updateRow()` on change:

```tsx
render(_, record, index) {
  return (
    <AInput
      value={record?.description ?? ''}
      onChange={(e) => updateRow(index, { description: e?.target?.value })}
      isLabelOnly={isLabelOnly}
      disabled={disabled}
    />
  );
}
```

**3. Calculation pipeline:**
When any cell changes, the component runs a calculation pipeline:

```
User edits cell → updateRow() → handleOnSave() → calculateProfitAndLossItems() → onSave()
```

**4. Conditional rendering based on `paymentBasis`:**
The Rate and Quantity columns render completely different UI based on whether the billing type is `LUMPSUM`, `PERCENTAGE`, or a rate-based type.

**5. Event bubbling to parent:**
All changes bubble up via `onSave(newItems)`. The parent is responsible for persisting data. The table component is **controlled** — it doesn't own its data.

#### How to Add a New Feature Like This

1. **Define your DTO types** (or use auto-generated ones from `http/app/models/`)
2. **Create API hooks** in `features/<feature>/api/`
3. **Build helper functions** for calculations in `features/<feature>/helpers/`
4. **Compose the UI** using atom components from `components/atoms/` and domain selects from `features/common/components/select/`
5. **Wire up data flow**: Parent fetches → passes to table → table emits changes → parent saves
6. **Add the page** in `app/(dashboard)/<route>/page.tsx`

---

## 6. Discussion & Improvement Suggestions

### What's Working Well

- **Consistent feature structure** — Each feature folder follows the same convention making it easy to navigate
- **Type-safe API layer** — Auto-generated types from OpenAPI prevent mismatches
- **Rich select library** — 100+ pre-built domain dropdowns save huge development time
- **Zustand + React Query combo** — Clean separation of server state vs. client state
- **Atomic component system** — `isLabelOnly` pattern enables edit/view mode toggling

### Areas for Improvement

#### 1. Component Size

Some components like `ProfitAndLossItemsTable` exceed 700 lines. Consider:

- **Extract column definitions** into a separate `useColumns()` hook or `columns.tsx` file
- **Extract handlers** into a `useTableHandlers()` hook
- **Split modal logic** into a separate `RestrictionModal` component

```
Before: ProfitAndLossItemsTable.tsx (700+ lines)
After:
  ├── ProfitAndLossItemsTable.tsx     (150 lines - composition)
  ├── usePLTableColumns.tsx           (300 lines - column definitions)
  ├── usePLTableHandlers.tsx          (150 lines - event handlers)
  └── RestrictionModal.tsx            (100 lines - modal component)
```

#### 2. Boolean Prop Proliferation

The `hide*Column` pattern leads to many boolean props. Consider using a **column configuration object** or **composition pattern** instead:

```tsx
// Instead of 10+ boolean props:
<PLTable hideTypeColumn hideCounterPartyColumn hideRateColumn ... />

// Consider a columns config:
<PLTable columns={['invoiceType', 'description', 'total', 'amount']} />

// Or compound component pattern:
<PLTable items={items} onSave={onSave}>
  <PLTable.InvoiceTypeColumn />
  <PLTable.DescriptionColumn />
  <PLTable.TotalColumn />
</PLTable>
```

#### 3. Mixed API Patterns

The codebase has two API patterns coexisting:

- **Modern:** `useAppQuery` / `useAppMutation` (openapi-fetch + react-query)
- **Legacy:** `axios` + `*Service` class calls

New code should exclusively use the modern pattern. Consider a systematic migration plan for legacy hooks.

#### 4. State Management Documentation

The existing `docs/state-management.md` references `swr` and `Formik`, which are not the primary tools anymore. Update to reflect the actual stack: React Query, Zustand, React Hook Form, nuqs.

#### 5. Testing Coverage

The `test/` folder contains test utilities, but test coverage across features appears inconsistent. Consider:

- Adding tests for helper/utility functions first (easiest win)
- Adding integration tests for API hooks using `msw` (Mock Service Worker)
- Adding tests for complex calculation functions like `calculateProfitAndLossItems`

#### 6. Missing Documentation

- `docs/deployment.md` is empty
- No documentation for the authentication flow (MSAL → NextAuth → token refresh)
- No documentation for the code generation pipeline (`yarn gen:api:app`)
- No architecture decision records (ADRs) for key decisions

#### 7. Consider Feature Barrel Exports

Each feature's `index.ts` should export a clean public API. Other features should only import from the barrel, not reach into internal folders:

```tsx
// ✅ Good — import from barrel
import { Estimate, useEstimateStore } from '@/features/estimate';

// ❌ Bad — reaching into internals
import { SomeHelper } from '@/features/estimate/helpers/someHelper';
```

#### 8. Error Boundary Strategy

Consider adding React Error Boundaries at the feature level so that one crashing module doesn't take down the entire app:

```tsx
// app/(dashboard)/estimate/layout.tsx
<ErrorBoundary fallback={<ErrorFallback />}>
  <VoyageEstimateStoreProvider>{children}</VoyageEstimateStoreProvider>
</ErrorBoundary>
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    BVMS Developer Cheat Sheet                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Start dev server:     yarn dev        (port 3333)          │
│  Run tests:            yarn test                            │
│  Lint:                 yarn lint:fix                        │
│  Type check:           yarn types                           │
│  Regen API types:      yarn gen:api:app / yarn gen:api:master│
│                                                             │
│  Server data?    → useAppQuery / useMasterQuery             │
│  Complex state?  → Zustand store                            │
│  Form fields?    → React Hook Form + Zod                    │
│  URL params?     → nuqs useQueryState                       │
│  Simple toggle?  → useState                                 │
│                                                             │
│  UI input?       → components/atoms/a-* (not raw antd)      │
│  Domain select?  → features/common/components/select/       │
│  Notifications?  → useNotification() from core/hooks        │
│  Loading state?  → <LoadingWrapper isLoading />             │
│                                                             │
│  New feature?    → features/<name>/{api,components,hooks,...}│
│  New page?       → app/(dashboard)/<route>/page.tsx         │
│  Shared code?    → core/ or features/common/                │
│                                                             │
│  NEVER mutate state — always spread/immer                   │
│  NEVER edit http/ files — they're auto-generated            │
│  ALWAYS use path aliases (@/... or @features/...)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
