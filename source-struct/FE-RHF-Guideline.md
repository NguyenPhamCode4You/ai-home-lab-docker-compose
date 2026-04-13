# Vessel Report – React Hook Form & React Query Developer Guide

> A step-by-step guide for new developers to understand (and follow) the data-fetching
> and form management patterns used in the **Vessel Report / Activities** feature.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Component Hierarchy](#2-component-hierarchy)
3. [Step 1 – Define the Zod Schema](#step-1--define-the-zod-schema)
4. [Step 2 – Create React Query API Hooks](#step-2--create-react-query-api-hooks)
5. [Step 3 – Build the Form Hook](#step-3--build-the-form-hook)
6. [Step 4 – Wrap with FormProvider](#step-4--wrap-with-formprovider)
7. [Step 5 – Consume Form in Child Components](#step-5--consume-form-in-child-components)
8. [Step 6 – Dynamic Arrays with useFieldArray](#step-6--dynamic-arrays-with-usefieldarray)
9. [Step 7 – Submit & Mutation Flow](#step-7--submit--mutation-flow)
10. [Performance Rules (Must-Read)](#performance-rules-must-read)
11. [Complete Data Flow Diagram](#complete-data-flow-diagram)
12. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)
13. [Appendix A – Making the Form Hook Generic](#appendix-a--making-the-form-hook-generic)

---

## 1. Architecture Overview

The Vessel Report feature follows a **layered architecture**:

```
┌─────────────────────────────────────────────────────────┐
│  Zod Schema          (single source of truth for types) │
├─────────────────────────────────────────────────────────┤
│  React Query Hooks   (server state: GET / mutations)    │
├─────────────────────────────────────────────────────────┤
│  Form Hook           (useForm + zodResolver + submit)   │
├─────────────────────────────────────────────────────────┤
│  FormProvider        (context bridge to child tree)     │
├─────────────────────────────────────────────────────────┤
│  Child Components    (useFormContext / Controller)       │
└─────────────────────────────────────────────────────────┘
```

**Key files:**

| Layer                | File                                                                                |
| -------------------- | ----------------------------------------------------------------------------------- |
| Schema               | `features/voyage/schemas/vesselReport.schema.ts`                                    |
| API hooks            | `features/voyage/api/useVesselReportAPI.ts`                                         |
| Form hook            | `features/voyage/hooks/useVesselReportForm.ts`                                      |
| FormProvider wrapper | `features/voyage/components/activities/ActivitiesReportDetail.tsx`                  |
| Child (general info) | `features/voyage/components/activities/ActivitiesReportDetailInformation.tsx`       |
| Child (bunker table) | `features/voyage/components/activities/ActivitiesReportDetailBunkerConsumption.tsx` |

---

## 2. Component Hierarchy

```
app/(dashboard)/voyage/[id]/activities/page.tsx
└── VoyageVesselReportPage
    └── PortActivitiesPage (split panel)
        ├── Left:  ActivitiesReportGeneral (report list table)
        └── Right: ActivitiesReportDetail  ← FormProvider lives here
            ├── AMap (interactive map)
            ├── ActivitiesReportDetailInformation  ← useFormContext
            └── ActivitiesReportDetailBunkerConsumption  ← useFormContext + useFieldArray
```

> **Rule**: Only ONE component calls `useForm()`. All children use `useFormContext()`.

---

## Step 1 – Define the Zod Schema

The schema is the **single source of truth** for form types and validation.

```typescript
// features/voyage/schemas/vesselReport.schema.ts
import { z } from 'zod';

// 1. Define nested schemas first
const bunkerConsumptionSchema = z.object({
  bunkerTypeId: z.string().nullable().optional(),
  remainingAmountInMetricTons: z.number().nullable().optional(),
  totalConsumptionInMetricTons: z.number().nullable().optional(),
  voyageBunkerLotId: z.string().nullable().optional(),
  id: z.string().nullable().optional(),
});

// 2. Define the main form schema
export const vesselReportSchema = z
  .object({
    voyageId: z.string().nullable().optional(),
    reportType: z
      .string()
      .nullable()
      .refine((val) => val !== null && val !== '', {
        message: 'Report type is required',
      }),
    lattitude: z.number().refine((val) => val == null || (val >= -90 && val <= 90), {
      message: 'Latitude must be between -90° and 90°',
    }),
    distanceTravelledInSeaMiles: z.number().nullable().optional(),
    bunkerConsumptions: z.array(bunkerConsumptionSchema).nullable().optional(),
    // ... more fields
  })
  .superRefine((data, ctx) => {
    // Cross-field validation
    if (data.reportType === 'Departure' && !data.timeOfArrival) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Time Of Arrival is required for Departure reports',
        path: ['timeOfArrival'],
      });
    }
  });

// 3. Infer the TypeScript type — NEVER manually define form types
export type VesselReportFormData = z.infer<typeof vesselReportSchema>;
```

### Why this matters

- Types are automatically derived — no type drift between validation and TypeScript.
- `.superRefine()` enables cross-field validation (e.g., field B required when field A = X).
- Nested schemas (`bunkerConsumptionSchema`) map directly to `useFieldArray` items.

---

## Step 2 – Create React Query API Hooks

Organize all API hooks in a dedicated file per feature.

### Query Keys (structured & consistent)

```typescript
// features/voyage/api/useVesselReportAPI.ts

// Hierarchical key structure enables targeted invalidation
export const vesselReportKeys = {
  all: ['vesselReport'] as const,
  lists: (voyageId: string) => [...vesselReportKeys.all, 'list', voyageId] as const,
  detail: (id: string | null | undefined) => [...vesselReportKeys.all, 'detail', id] as const,
};

// Separate mutation keys for tracking pending state
export const vesselReportMutationKeys = {
  update: ['vesselReports', 'update'] as const,
  create: ['vesselReports', 'create'] as const,
  approve: ['vesselReports', 'approve'] as const,
};
```

### GET Hook (useQuery)

```typescript
export const useVesselReport = (id?: string, options?: any) => {
  return useQuery<VesselReportCrudDto, Error>({
    queryKey: vesselReportKeys.detail(id),
    queryFn: () => {
      if (!id) throw new Error('Vessel Report ID is required');
      return VesselReportService.getVesselReport(id);
    },
    staleTime: Infinity, // Don't auto-refetch: we invalidate explicitly
    enabled: !!id, // Skip query when ID is missing
    ...options,
  });
};
```

### Mutation Hook (useMutation)

```typescript
export const useUpdateVesselReport = (id?: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: vesselReportMutationKeys.update,
    mutationFn: ({ vesselReportCrud }: { vesselReportCrud: VesselReportCrudDto }) =>
      VesselReportService.putVesselReport(id!, vesselReportCrud),
    onSuccess: () => {
      // Refetch all vessel report queries to keep UI in sync
      return queryClient.refetchQueries({ queryKey: vesselReportKeys.all });
    },
  });
};

export const useCreateVesselReport = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: vesselReportMutationKeys.create,
    mutationFn: async ({ vesselReportCrud }: { vesselReportCrud: VesselReportCrudDto }) =>
      VesselReportService.postVesselReport(vesselReportCrud),
    onSuccess: () => {
      return queryClient.refetchQueries({ queryKey: vesselReportKeys.all });
    },
  });
};
```

### Key Patterns

| Pattern                         | Example                          | Why                                            |
| ------------------------------- | -------------------------------- | ---------------------------------------------- |
| `staleTime: Infinity`           | GET hooks                        | Data is invalidated explicitly after mutations |
| `enabled: !!id`                 | Conditional fetching             | Prevents requests with missing params          |
| `refetchQueries` in `onSuccess` | After create/update              | Keeps all list & detail queries fresh          |
| Structured query keys           | `['vesselReport', 'detail', id]` | Enables granular cache invalidation            |

---

## Step 3 – Build the Form Hook

This custom hook is the **bridge** between server state (React Query) and form state (RHF).

```typescript
// features/voyage/hooks/useVesselReportForm.ts

export const useVesselReportForm = ({ isNew, reportId, voyageId }) => {
  // ── 1. Fetch server data ──
  const { data: existingReportData, isLoading } = useVesselReport(reportId, {
    enabled: !isNew && !!reportId,
  });

  // ── 2. Initialize form with zodResolver ──
  const methods = useForm<VesselReportFormData>({
    resolver: zodResolver(vesselReportSchema),
    defaultValues: { voyageId, ...defaultValues },
    mode: 'onBlur', // Validate when user leaves a field
  });

  const { getValues, setValue, watch, formState, trigger } = methods;

  // ── 3. Sync server data → form on load ──
  useEffect(() => {
    if (existingReportData && !isNew) {
      methods.reset({ ...defaultValues, ...existingReportData }, { keepDirty: false });
    }
  }, [existingReportData, isNew]);

  // ── 4. Setup mutations ──
  const { mutate: updateVesselReport, isPending: isUpdatePending } =
    useUpdateVesselReport(reportId);
  const { mutate: createVesselReport, isPending: isCreatePending } = useCreateVesselReport();

  // ── 5. Submit handler ──
  const onSubmit = async () => {
    const values = getValues();

    // Validate non-array fields
    const partialFields = (Object.keys(values) as Array<keyof VesselReportFormData>).filter(
      (k) => k !== 'bunkerConsumptions' && k !== 'bunkerReceivals'
    );
    const ok = await trigger(partialFields);
    if (!ok) return;

    const submissionData = { voyageId, ...values };

    if (isNew) {
      createVesselReport(
        { vesselReportCrud: submissionData },
        {
          onSuccess(data) {
            // Reset form to server-confirmed data
            methods.reset({ ...values, ...data, voyageId }, { keepDirty: false });
          },
        }
      );
    } else {
      updateVesselReport(
        { vesselReportCrud: { ...existingReportData, ...submissionData } },
        {
          onSuccess(data) {
            methods.reset({ ...submissionData, ...data }, { keepDirty: false });
          },
        }
      );
    }
  };

  // ── 6. Watch reactive values needed by parent ──
  const currentLattitude = watch('lattitude');
  const currentLongtitude = watch('longtitude');
  const reportType = watch('reportType');

  return {
    methods, // pass to <FormProvider>
    formState,
    existingReportData,
    reportType,
    currentLattitude,
    currentLongtitude,
    isLoading,
    isSubmitting: isUpdatePending || isCreatePending,
    onSubmit,
  };
};
```

### Data Flow Summary

```
Server (API)  ──useQuery──▶  existingReportData
                                    │
                            useEffect + reset()
                                    ▼
                              RHF Form State  ◀──── User edits fields
                                    │
                              onSubmit + getValues()
                                    ▼
                            useMutation  ──POST/PUT──▶  Server
                                    │
                             onSuccess + reset()
                                    ▼
                              Form synced with server
```

---

## Step 4 – Wrap with FormProvider

The **parent component** creates the form context. All children access it via `useFormContext()`.

```tsx
// features/voyage/components/activities/ActivitiesReportDetail.tsx

const ActivitiesReportDetail = ({ isNew }: { isNew: boolean }) => {
  const { methods, formState, reportType, onSubmit, currentVesselComparison, isSubmitting } =
    useVesselReportForm({ isNew, reportId, voyageId });

  return (
    // FormProvider bridges useForm → all descendants
    <FormProvider {...methods}>
      <form className="flex flex-col gap-2">
        {/* Header with Save/Approve buttons */}
        <div className="flex justify-between">
          <span>Activity Report</span>
          {formState.isDirty && (
            <AButton type="primary" loading={isSubmitting} onClick={onSubmit}>
              {isNew ? 'Create' : 'Update'}
            </AButton>
          )}
        </div>

        {/* Children — they access form via useFormContext */}
        <ActivitiesReportDetailInformation />
        <ActivitiesReportDetailBunkerConsumption />
      </form>
    </FormProvider>
  );
};
```

> **Rule:** `<FormProvider>` should be placed as **high as needed, but no higher**.
> It wraps only the components that need form access—not the entire page.

---

## Step 5 – Consume Form in Child Components

### Using Controller (for individual fields)

`Controller` isolates re-renders to the field that changed.

```tsx
// Inside a child component
import { Controller, useFormContext } from 'react-hook-form';

const DistanceField = () => {
  const { control } = useFormContext<VesselReportFormData>();

  return (
    <Controller
      control={control}
      name="distanceTravelledInSeaMiles"
      render={({ field, fieldState }) => (
        <div>
          <AInputNumber
            value={field.value ?? 0}
            onChange={(val) => field.onChange(val)}
            status={fieldState.error ? 'error' : undefined}
          />
          {fieldState.error && <span className="text-red-500">{fieldState.error.message}</span>}
        </div>
      )}
    />
  );
};
```

### Using useWatch (for reactive derived values)

`useWatch` subscribes to **specific fields only** — far more efficient than `watch()` or `getValues()`.

```tsx
import { useWatch, useFormContext } from 'react-hook-form';

const BunkerSummary = () => {
  const { control } = useFormContext<VesselReportFormData>();

  // Only re-renders when bunkerConsumptions changes
  const bunkerConsumptions = useWatch({
    control,
    name: 'bunkerConsumptions',
  });

  const totalConsumption = useMemo(
    () =>
      bunkerConsumptions?.reduce((sum, b) => sum + (b.totalConsumptionInMetricTons ?? 0), 0) ?? 0,
    [bunkerConsumptions]
  );

  return <span>Total: {totalConsumption} MT</span>;
};
```

---

## Step 6 – Dynamic Arrays with useFieldArray

For repeating rows (bunker consumptions, bunker receivals), use `useFieldArray`.

```tsx
import { useFieldArray, useFormContext, useWatch, Controller } from 'react-hook-form';

const BunkerConsumptionTable = () => {
  const { control } = useFormContext<VesselReportFormData>();

  // useFieldArray manages the array CRUD
  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'bunkerConsumptions',
  });

  // useWatch subscribes to the array for derived calculations
  const bunkerConsumptions = useWatch({ control, name: 'bunkerConsumptions' });

  const handleRemainingChange = (index: number, newValue: number) => {
    const current = bunkerConsumptions?.[index];
    if (!current) return;

    const previous = current.previousAmountInMetricTons ?? 0;
    const totalConsumption = Math.max(0, previous - newValue);

    // update() replaces the entire row immutably
    update(index, {
      ...current,
      remainingAmountInMetricTons: newValue,
      totalConsumptionInMetricTons: totalConsumption,
    });
  };

  return (
    <table>
      <tbody>
        {fields.map((field, index) => (
          <tr key={field.id}>
            <td>
              <Controller
                control={control}
                name={`bunkerConsumptions.${index}.remainingAmountInMetricTons`}
                render={({ field: f, fieldState }) => (
                  <AInputNumber
                    value={f.value ?? 0}
                    onChange={(val) => handleRemainingChange(index, val ?? 0)}
                    status={fieldState.error ? 'error' : undefined}
                  />
                )}
              />
            </td>
            <td>
              <button onClick={() => remove(index)}>Remove</button>
            </td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr>
          <td>
            <button onClick={() => append({ bunkerTypeId: null, remainingAmountInMetricTons: 0 })}>
              Add Row
            </button>
          </td>
        </tr>
      </tfoot>
    </table>
  );
};
```

### Key Rules

| Do                                          | Don't                               |
| ------------------------------------------- | ----------------------------------- |
| Use `field.id` as the `key` prop            | Use array `index` as the `key`      |
| Use `update(index, newRow)` for row changes | Mutate the existing object in place |
| Use `useWatch` for derived calculations     | Use `getValues()` at render time    |

---

## Step 7 – Submit & Mutation Flow

### The complete submit cycle

```
User clicks "Save"
     │
     ▼
onSubmit()
     │
     ├── getValues()          → snapshot all form fields
     ├── trigger(fields)      → validate (zodResolver runs)
     │      └── Fails? → errors shown via fieldState.error, return early
     │
     ├── Build submissionData  → merge form values with metadata
     │
     ├── createVesselReport() or updateVesselReport()
     │      │
     │      ├── onSuccess:
     │      │     ├── methods.reset(serverData)  → sync form to confirmed data
     │      │     └── queryClient.refetchQueries()  → refresh lists
     │      │
     │      └── onError:
     │            └── showError(message)
     │
     └── Done. formState.isDirty resets to false.
```

### Why `reset()` after mutation?

```typescript
// After server confirms the save:
methods.reset({ ...submissionData, ...serverResponse }, { keepDirty: false });
```

This does three things:

1. Updates `defaultValues` to the server-confirmed state
2. Resets `formState.isDirty` to `false` (Save button hides)
3. Preserves current form values while marking them as "clean"

---

## Performance Rules (Must-Read)

These rules prevent the re-render issues we've encountered in this codebase.

### ❌ Anti-Pattern: `getValues()` at render time

```tsx
// BAD — reads ALL fields, rebuilds on every re-render
const formValues = getValues();
const reportType = formValues.reportType;
const voyageId = formValues.voyageId;
```

### ✅ Correct: `useWatch` for specific fields

```tsx
// GOOD — only re-renders when these specific fields change
const [reportType, voyageId] = useWatch({
  control,
  name: ['reportType', 'voyageId'],
});
```

### ❌ Anti-Pattern: Destructuring `errors` from `formState`

```tsx
// BAD — subscribes to ALL error changes across ALL fields
const {
  formState: { errors },
} = useFormContext();

// Then used deep in the render tree:
<AInput status={errors.distanceTravelledInSeaMiles ? 'error' : undefined} />;
```

### ✅ Correct: Use `fieldState.error` inside Controller

```tsx
// GOOD — error is scoped to this single field
<Controller
  name="distanceTravelledInSeaMiles"
  render={({ field, fieldState }) => (
    <AInputNumber
      value={field.value}
      onChange={field.onChange}
      status={fieldState.error ? 'error' : undefined}
    />
  )}
/>
```

### Summary Table

| Pattern                          | Scope            | Re-renders when                                                       |
| -------------------------------- | ---------------- | --------------------------------------------------------------------- |
| `watch('field')`                 | Component        | That field changes                                                    |
| `useWatch({ name: 'field' })`    | Component        | That field changes (works in children)                                |
| `useWatch({ name: ['a', 'b'] })` | Component        | Either field changes                                                  |
| `getValues()`                    | None (snapshot)  | **Never** triggers re-render—but stale if component doesn't re-render |
| `formState: { errors }`          | **Entire form**  | **Any** field error changes                                           |
| `Controller` render              | **Single field** | Only that field changes                                               |
| `fieldState.error`               | **Single field** | Only that field's error changes                                       |

### Decision Guide

```
Need a field value for conditional rendering?
  → useWatch({ name: 'fieldName' })

Need a field value only in an event handler (onClick, onSubmit)?
  → getValues('fieldName')  (no subscription needed)

Need to show validation errors?
  → Use fieldState.error inside Controller (NEVER destructure errors at top level)

Need to show/edit a form field?
  → Controller with render prop
```

---

## Complete Data Flow Diagram

```
                        ┌─────────────────────┐
                        │   Zod Schema         │
                        │   (vesselReport      │
                        │    Schema.ts)         │
                        └──────────┬────────────┘
                                   │ types + validation
                    ┌──────────────┼──────────────────┐
                    ▼              ▼                   ▼
          ┌──────────────┐  ┌───────────────┐  ┌────────────────┐
          │ API Hooks     │  │ Form Hook     │  │ Child          │
          │ (useQuery     │  │ (useForm +    │  │ Components     │
          │  useMutation) │  │  zodResolver) │  │ (Controller)   │
          └──────┬───────┘  └───────┬───────┘  └───────┬────────┘
                 │                  │                   │
    fetch ───────┘    reset() ◀─────┘                   │
                 │                  │                   │
                 ▼                  ▼                   │
          ┌──────────────────────────────┐             │
          │     FormProvider             │             │
          │     (ActivitiesReportDetail) │◀────────────┘
          └──────────────────────────────┘   useFormContext()
                        │
              onSubmit → getValues → mutation → onSuccess → reset
```

---

## Quick Reference Cheat Sheet

### File Organization (for a new feature)

```
features/my-feature/
├── schemas/
│   └── myFeature.schema.ts          ← Zod schema + inferred type
├── api/
│   └── useMyFeatureAPI.ts           ← query keys + useQuery + useMutation
├── hooks/
│   └── useMyFeatureForm.ts          ← useForm + server sync + submit logic
├── components/
│   ├── MyFeatureFormWrapper.tsx      ← FormProvider here
│   ├── MyFeatureGeneralInfo.tsx      ← useFormContext + Controller
│   └── MyFeatureItemsTable.tsx       ← useFieldArray + useWatch
└── pages/
    └── MyFeaturePage.tsx             ← page entry point
```

### Import Map

```typescript
// Schema
import { myFeatureSchema, type MyFeatureFormData } from '../schemas/myFeature.schema';

// API
import { useMyFeature, useUpdateMyFeature } from '../api/useMyFeatureAPI';

// Form setup
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FormProvider } from 'react-hook-form';

// In children
import { useFormContext, Controller, useWatch, useFieldArray } from 'react-hook-form';
```

### Quick Validation Modes

| Mode       | When it validates        | Our choice               |
| ---------- | ------------------------ | ------------------------ |
| `onBlur`   | When user leaves a field | ✅ Used in Vessel Report |
| `onChange` | On every keystroke       | Too aggressive           |
| `onSubmit` | Only when form submits   | Good for simple forms    |
| `all`      | onChange + onBlur        | Maximum feedback         |

---

## Appendix A – Making the Form Hook Generic

### The Problem

Every feature re-invents the same form lifecycle:

```
fetch data → init form → user edits → validate → mutate → reset → sync dirty state
```

Compare `useVesselReportForm`, `useBunkerOrderDetailForm`, `useShipmentDetailForm` — all repeat:

1. `useForm()` with `zodResolver`
2. `useQuery()` to fetch existing data
3. `useEffect()` to `reset()` form when data arrives
4. `useMutation()` for create / update
5. `onSubmit()` that validates, then calls create or update
6. `reset()` after mutation success
7. Dirty state tracking (`useAlertUnsaveChangedContext`)

This is the same boilerplate pattern `ApiSelect` eliminated for dropdowns with `Setting<T>`.

### Inspiration: How `ApiSelect` Works

`ApiSelect` is **one component** that handles ALL dropdowns in the app. Each feature only provides a `Setting<T>` config object:

```typescript
// The generic contract — each feature only defines THIS:
type Setting<T> = {
  name: string;
  search: (params?) => Promise<T[]>;        // how to fetch options
  getById?: (id) => Promise<T | null>;       // how to resolve a selected value
  render: (item: T) => DefaultOptionType;    // how to display an option
  create?: (key: string) => Promise<T>;      // optional inline creation
};

// Usage: BunkerTypes select — ZERO boilerplate
const setting: Setting<BunkerTypeDto> = {
  name: 'select/bunker-types',
  search: (params) => BunkerTypesService.postBunkerTypesSearch(params),
  getById: (id) => BunkerTypesService.getBunkerTypes(id),
  render: (dto) => ({ label: dto.bunkerTypeCode, value: dto.id }),
};

<ApiSelect setting={setting} {...props} />
```

**What makes this powerful:**

- Feature developers only describe _what_ (data shape, API calls, display logic)
- `ApiSelect` handles the _how_ (loading, pagination, search debounce, caching)

We can apply the same principle to form hooks.

---

### Step 1 – Define the Generic Config Type

```typescript
// features/common/hooks/useFeatureForm/types.ts

import { FieldValues, Path, UseFormProps } from 'react-hook-form';
import { UseMutationResult, UseQueryResult } from '@tanstack/react-query';
import { ZodSchema } from 'zod';

/**
 * Configuration object for a standard CRUD form.
 * Similar to Setting<T> for ApiSelect — the developer only describes
 * the data shape, API calls, and business-specific transforms.
 */
export interface FormConfig<
  TFormData extends FieldValues,
  TServerData,
  TCreateResponse = TServerData,
  TUpdateResponse = TServerData,
> {
  /** Zod schema — validation + TypeScript type generation */
  schema: ZodSchema<TFormData>;

  /** RHF validation mode */
  mode?: UseFormProps<TFormData>['mode'];

  /** Default values for a new (empty) form */
  defaultValues: TFormData;

  /** Query hook that fetches the existing record */
  useGetData: (
    id: string | undefined,
    options?: { enabled: boolean }
  ) => UseQueryResult<TServerData>;

  /** Mutation hook for creating a new record */
  useCreate: () => UseMutationResult<TCreateResponse, Error, { data: TServerData }>;

  /** Mutation hook for updating an existing record */
  useUpdate: (id?: string) => UseMutationResult<TUpdateResponse, Error, { data: TServerData }>;

  /** Transform server data → form shape (called inside the reset effect) */
  serverToForm: (serverData: TServerData, defaults: TFormData) => TFormData;

  /** Transform form values → API payload (called before mutation) */
  formToServer: (formValues: TFormData, existing?: TServerData) => TServerData;

  /** Fields to exclude from pre-submit validation (e.g. nested arrays) */
  skipValidationFields?: Path<TFormData>[];

  /** Called after a successful create/update with the server response */
  onMutationSuccess?: (data: TCreateResponse | TUpdateResponse, isNew: boolean) => void;
}
```

### Step 2 – Build the Generic Hook

```typescript
// features/common/hooks/useFeatureForm/useFeatureForm.ts

import { useEffect } from 'react';
import { FieldValues, Path, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAlertUnsaveChangedContext } from '@/features/common/context/AlertUnsaveFormContext';
import { FormConfig } from './types';

interface UseFeatureFormParams<TFormData extends FieldValues, TServerData> {
  config: FormConfig<TFormData, TServerData>;
  isNew: boolean;
  recordId?: string;
  /** Extra default-value overrides (e.g. voyageId from URL) */
  extraDefaults?: Partial<TFormData>;
}

export function useFeatureForm<TFormData extends FieldValues, TServerData>({
  config,
  isNew,
  recordId,
  extraDefaults,
}: UseFeatureFormParams<TFormData, TServerData>) {
  const { setIsDirty } = useAlertUnsaveChangedContext();

  // ── 1. Fetch existing data ──
  const { data: serverData, isLoading: isFetching } = config.useGetData(recordId, {
    enabled: !isNew && !!recordId,
  });

  // ── 2. Create mutations ──
  const { mutate: create, isPending: isCreating } = config.useCreate();
  const { mutate: update, isPending: isUpdating } = config.useUpdate(recordId);

  // ── 3. Initialize form ──
  const methods = useForm<TFormData>({
    resolver: zodResolver(config.schema),
    defaultValues: { ...config.defaultValues, ...extraDefaults } as any,
    mode: config.mode ?? 'onBlur',
  });

  const { getValues, trigger, formState } = methods;

  // ── 4. Sync server data → form ──
  useEffect(() => {
    if (!isNew && serverData) {
      const formData = config.serverToForm(serverData, config.defaultValues);
      methods.reset({ ...formData, ...extraDefaults } as any, { keepDirty: false });
    }
  }, [serverData, isNew]);

  // ── 5. Reset for new records ──
  useEffect(() => {
    if (isNew) {
      methods.reset({ ...config.defaultValues, ...extraDefaults } as any, { keepDirty: false });
    }
  }, [isNew]);

  // ── 6. Dirty state tracking ──
  useEffect(() => {
    setIsDirty(formState.isDirty);
  }, [formState.isDirty, setIsDirty]);

  // ── 7. Submit handler ──
  const onSubmit = async () => {
    const values = getValues();

    // Validate everything except skipped fields (e.g. nested arrays)
    const skip = new Set(config.skipValidationFields ?? []);
    const fieldsToValidate = (Object.keys(values) as Path<TFormData>[]).filter((k) => !skip.has(k));

    const ok = await trigger(fieldsToValidate);
    if (!ok) return;

    const payload = config.formToServer(values, serverData ?? undefined);

    if (isNew) {
      create(
        { data: payload },
        {
          onSuccess(data) {
            methods.reset(config.serverToForm(data as any, values), { keepDirty: false });
            config.onMutationSuccess?.(data, true);
          },
        }
      );
    } else {
      update(
        { data: payload },
        {
          onSuccess(data) {
            methods.reset(config.serverToForm(data as any, values), { keepDirty: false });
            config.onMutationSuccess?.(data, false);
          },
        }
      );
    }
  };

  return {
    methods, //  pass to <FormProvider>
    formState,
    serverData, //  raw server record (for comparison, etc.)
    isLoading: isFetching || isCreating || isUpdating,
    isSubmitting: isCreating || isUpdating,
    onSubmit,
  };
}
```

### Step 3 – Use It in a Feature

Now a developer creating a **new** feature only writes:

```typescript
// features/my-feature/hooks/useMyFeatureForm.ts

import { useFeatureForm, FormConfig } from '@/features/common/hooks/useFeatureForm';
import { myFeatureSchema, MyFeatureFormData } from '../schemas/myFeature.schema';
import { useMyFeature, useCreateMyFeature, useUpdateMyFeature } from '../api/useMyFeatureAPI';
import { MyFeatureDto } from '@/http/app';

// ① Define the config — this is the ONLY custom part
const config: FormConfig<MyFeatureFormData, MyFeatureDto> = {
  schema: myFeatureSchema,
  mode: 'onBlur',

  defaultValues: {
    name: '',
    status: null,
    items: [],
  },

  // ② Plug in your API hooks
  useGetData: useMyFeature,
  useCreate: useCreateMyFeature,
  useUpdate: useUpdateMyFeature,

  // ③ Map server shape ↔ form shape
  serverToForm: (server, defaults) => ({
    ...defaults,
    ...server,
    name: server.name ?? '',
    status: server.status ?? null,
    items: server.items ?? [],
  }),

  formToServer: (form) => ({
    ...form,
    items: form.items ?? [],
  }),

  // ④ Nested arrays skip top-level validation
  skipValidationFields: ['items'],

  onMutationSuccess: (data, isNew) => {
    if (isNew && data?.id) {
      // navigate to edit route, update store, etc.
    }
  },
};

// ⑤ The hook itself is now a ONE-LINER
export function useMyFeatureForm(params: { isNew: boolean; recordId?: string }) {
  return useFeatureForm({
    config,
    isNew: params.isNew,
    recordId: params.recordId,
    extraDefaults: { voyageId: params.voyageId },
  });
}
```

### Step 4 – Extend for Feature-Specific Logic

The generic hook returns `methods`, so you can still layer feature-specific behavior on top:

```typescript
export function useMyFeatureForm(params: { isNew: boolean; recordId?: string }) {
  // Generic lifecycle
  const base = useFeatureForm({ config, ...params });

  // Feature-specific additions
  const reportType = base.methods.watch('reportType');

  const onApprove = () => {
    base.methods.clearErrors(['items']);
    base.methods.handleSubmit(() => approveMutation({ id: params.recordId }))();
  };

  return {
    ...base,
    reportType, // feature-specific reactive value
    onApprove, // feature-specific action
  };
}
```

---

### Side-by-Side Comparison

| Aspect                     | Before (copy-paste)            | After (generic)                        |
| -------------------------- | ------------------------------ | -------------------------------------- |
| `useForm` + resolver setup | ~10 lines per feature          | 0 (handled by `useFeatureForm`)        |
| Server → form reset effect | ~20 lines per feature          | 0 (handled by `useFeatureForm`)        |
| Submit handler boilerplate | ~30 lines per feature          | 0 (handled by `useFeatureForm`)        |
| Dirty state tracking       | 5 lines per feature            | 0 (handled by `useFeatureForm`)        |
| **Developer writes**       | ~80 lines of repeated plumbing | **Only the config object** (~30 lines) |
| Feature-specific logic     | Mixed in with boilerplate      | Layered on top cleanly                 |

---

### The Pattern Applied to Existing Features

Here is how the existing `useVesselReportForm` maps to the generic config:

```typescript
const vesselReportConfig: FormConfig<VesselReportFormData, VesselReportCrudDto> = {
  schema: vesselReportSchema,
  mode: 'onBlur',
  defaultValues, // already defined at file top

  useGetData: useVesselReport,
  useCreate: useCreateVesselReport,
  useUpdate: useUpdateVesselReport,

  serverToForm: (server, defaults) => ({
    ...defaults,
    ...server,
    shouldUseInPortDepartureTimeForItinerary:
      server.shouldUseInPortDepartureTimeForItinerary ?? false,
    timeOfReport: server.timeOfReport ?? null,
    reportType: server.reportType ?? '',
    lattitude: server.lattitude ?? 0,
    longtitude: server.longtitude ?? 0,
    // ... other null-coalescing transforms
  }),

  formToServer: (form, existing) => ({
    ...existing,
    ...form,
    source: form.source ?? undefined,
    bunkerConsumptions: form.bunkerConsumptions ?? [],
  }),

  skipValidationFields: ['bunkerConsumptions', 'bunkerReceivals'],
};
```

Then the feature-specific additions (geo calculation, approval flow, WFOS comparison) are layered on top — keeping the config clean and the plumbing automated.

---

### Generic API Hook Factory (Bonus)

Apply the same principle to React Query hooks. Instead of writing 5 near-identical hooks per feature, define a factory:

```typescript
// features/common/hooks/useFeatureForm/createApiHooks.ts

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

interface ApiHookConfig<TDto> {
  /** Base key for all queries, e.g. 'vesselReport' */
  baseKey: string;

  /** GET single record */
  getById: (id: string) => Promise<TDto>;

  /** GET list */
  getList?: (params: any) => Promise<TDto[]>;

  /** POST create */
  create?: (data: TDto) => Promise<TDto>;

  /** PUT update */
  update?: (id: string, data: TDto) => Promise<TDto>;

  /** DELETE */
  remove?: (id: string) => Promise<void>;
}

export function createApiHooks<TDto>(cfg: ApiHookConfig<TDto>) {
  const keys = {
    all: [cfg.baseKey] as const,
    detail: (id?: string) => [cfg.baseKey, 'detail', id] as const,
    list: (...args: any[]) => [cfg.baseKey, 'list', ...args] as const,
  };

  const useGet = (id?: string, options?: { enabled?: boolean }) =>
    useQuery<TDto>({
      queryKey: keys.detail(id),
      queryFn: () => cfg.getById(id!),
      enabled: !!id && (options?.enabled ?? true),
      staleTime: Infinity,
    });

  const useCreate = () => {
    const qc = useQueryClient();
    return useMutation({
      mutationFn: ({ data }: { data: TDto }) => cfg.create!(data),
      onSuccess: () => qc.refetchQueries({ queryKey: keys.all }),
    });
  };

  const useUpdate = (id?: string) => {
    const qc = useQueryClient();
    return useMutation({
      mutationFn: ({ data }: { data: TDto }) => cfg.update!(id!, data),
      onSuccess: () => qc.refetchQueries({ queryKey: keys.all }),
    });
  };

  return { keys, useGet, useCreate, useUpdate };
}
```

Usage:

```typescript
// features/voyage/api/useVesselReportAPI.ts (simplified)

const vesselReportApi = createApiHooks<VesselReportCrudDto>({
  baseKey: 'vesselReport',
  getById: (id) => VesselReportService.getVesselReport(id),
  create: (data) => VesselReportService.postVesselReport(data),
  update: (id, data) => VesselReportService.putVesselReport(id, data),
});

// Destructure what you need
export const { useGet: useVesselReport, useCreate: useCreateVesselReport } = vesselReportApi;

// Feature-specific hooks (approve, draft, etc.) are still defined manually
export const useApproveVesselReport = (errorCallback?) => {
  /* ... */
};
```

---

### Decision Matrix: When to Use Each Approach

| Scenario                                          | Approach                                               |
| ------------------------------------------------- | ------------------------------------------------------ |
| Standard CRUD form (create + edit + save)         | `useFeatureForm` with a config object                  |
| Form with extra actions (approve, calculate, geo) | `useFeatureForm` + layer custom methods on top         |
| Form embedded inside another provider (wizard)    | Use `useFormContext` directly — no generic hook needed |
| Lightweight filter/export form                    | `useCustomForm` (existing) — no server sync needed     |
| Read-only detail view (no form)                   | `useQuery` only — no form hook at all                  |
