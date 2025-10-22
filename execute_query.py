import pandas as pd

def execute_query(df: pd.DataFrame, query_dict: dict):
    try:
        # -------------------------
        # Basic setup
        # -------------------------
        if "error" in query_dict:
            return query_dict["error"]

        df_filtered = df.copy()
        op = query_dict.get("operation")
        cols = query_dict.get("columns") or [query_dict.get("column")]
        cols = [c for c in cols if c in df_filtered.columns]
        group_col = query_dict.get("group_by")
        top_n = query_dict.get("top_n", 1)
        filters = query_dict.get("filter", {})

        # -------------------------
        # Apply filters dynamically
        # -------------------------
        for col, val in filters.items():
            if col in df_filtered.columns:
                if isinstance(val, list) and len(val) == 2:
                    df_filtered = df_filtered[
                        (df_filtered[col] >= val[0]) & (df_filtered[col] <= val[1])
                    ]
                else:
                    df_filtered = df_filtered[df_filtered[col] == val]

        # -------------------------
        # Drop duplicates for medal-related operations
        # -------------------------
        if "Medal" in df_filtered.columns and op in ["sum", "count", "top"]:
            df_filtered = df_filtered.drop_duplicates(
                subset=['Team', 'NOC', 'Year', 'Sport', 'Event', 'Medal']
            )

        # -------------------------
        # Metadata operation
        # -------------------------
        if op == "metadata":
            key = query_dict.get("metadata_key")
            if key in df_filtered.columns:
                return {key: df_filtered[key].nunique()}
            else:
                return f"Metadata key '{key}' not found in dataset."

        # -------------------------
        # Unique count
        # -------------------------
        if op == "unique_count":
            if not cols:
                return "Error: No valid column found for unique_count."
            count = df_filtered[cols[0]].nunique()
            return {f"Unique count of {cols[0]}": int(count)}

        # -------------------------
        # Top N or nth place operation
        # -------------------------
        if op == "top":
            if not group_col or not cols:
                return "Error: 'top' operation requires group_by and columns."
            
            grouped = df_filtered.groupby(group_col)[cols].sum().reset_index()
            grouped = grouped.sort_values(cols[0], ascending=False).reset_index(drop=True)

            # nth_place support
            if "nth_place" in query_dict:
                n = query_dict["nth_place"]
                if 1 <= n <= len(grouped):
                    result = grouped.iloc[[n-1]]  # 0-based index
                else:
                    result = f"Error: nth_place {n} is out of range (max {len(grouped)})."
            else:
                # fallback to top_n (default 1)
                result = grouped.head(top_n)

            return result.reset_index(drop=True)

        # -------------------------
        # Aggregation operations
        # -------------------------
        if not cols:
            return "Error: No valid columns for aggregation."

        if group_col:
            grouped = df_filtered.groupby(group_col)[cols]

            if op == "sum":
                result = grouped.sum().reset_index()
            elif op == "mean":
                result = grouped.mean().reset_index()
            elif op == "max":
                result = grouped.max().reset_index()
            elif op == "min":
                result = grouped.min().reset_index()
            elif op == "count":
                grouped = (
                    df_filtered.drop_duplicates(subset=[group_col] + cols)
                    .groupby(group_col)[cols[0]]
                    .nunique()
                    .reset_index()
                )
                result = grouped
            else:
                result = "Operation not recognized."

            return result

        else:
            # No group_by — direct aggregations
            if op == "sum":
                return df_filtered[cols].sum().to_dict()
            elif op == "mean":
                return df_filtered[cols].mean().to_dict()
            elif op == "max":
                return df_filtered[cols].max().to_dict()
            elif op == "min":
                return df_filtered[cols].min().to_dict()
            elif op == "count":
                df_filtered = df_filtered.drop_duplicates(subset=cols)
                return {cols[0]: int(df_filtered[cols[0]].nunique())}
            else:
                return "Operation not recognized."

    except Exception as e:
        return f"Error executing query: {e}"
