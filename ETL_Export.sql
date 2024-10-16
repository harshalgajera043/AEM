
-- Connect to NetSuite database
-- Assuming the connection is established using a NetSuite ODBC/JDBC driver
-- Extract data from various tables: Sales Orders, Purchase Orders, Work Orders, Transfer Orders, and Inventory Adjustments
-- Example: SELECT * FROM sales_orders WHERE order_date >= '2024-01-01';

WITH sales_data AS (
  SELECT 
    product_id, 
    SUM(quantity_sold) AS total_sales, 
    DATE_TRUNC('month', order_date) AS sales_month
  FROM 
    sales_orders
  WHERE 
    order_date >= '2024-01-01'
  GROUP BY 
    product_id, DATE_TRUNC('month', order_date)
),
inventory_data AS (
  SELECT 
    product_id, 
    AVG(current_stock_level) AS avg_inventory_level
  FROM 
    inventory
  WHERE 
    stock_check_date >= '2024-01-01'
  GROUP BY 
    product_id
),
purchase_orders AS (
  SELECT 
    product_id, 
    SUM(order_quantity) AS total_purchase_orders
  FROM 
    purchase_orders
  WHERE 
    order_date >= '2024-01-01'
  GROUP BY 
    product_id
),
work_orders AS (
  SELECT 
    product_id, 
    SUM(work_order_quantity) AS total_work_orders
  FROM 
    work_orders
  WHERE 
    order_date >= '2024-01-01'
  GROUP BY 
    product_id
),
transfer_orders AS (
  SELECT 
    product_id, 
    SUM(transfer_quantity) AS total_transfer_orders
  FROM 
    transfer_orders
  WHERE 
    transfer_date >= '2024-01-01'
  GROUP BY 
    product_id
),
inventory_adjustments AS (
  SELECT 
    product_id, 
    SUM(adjustment_quantity) AS total_inventory_adjustments
  FROM 
    inventory_adjustments
  WHERE 
    adjustment_date >= '2024-01-01'
  GROUP BY 
    product_id
)
SELECT 
  s.product_id, 
  p.product_name, 
  s.sales_month, 
  s.total_sales, 
  i.avg_inventory_level, 
  po.total_purchase_orders, 
  wo.total_work_orders, 
  to.total_transfer_orders, 
  ia.total_inventory_adjustments
FROM 
  sales_data s
JOIN 
  inventory_data i ON s.product_id = i.product_id
JOIN 
  purchase_orders po ON s.product_id = po.product_id
JOIN 
  work_orders wo ON s.product_id = wo.product_id
JOIN 
  transfer_orders to ON s.product_id = to.product_id
JOIN 
  inventory_adjustments ia ON s.product_id = ia.product_id
JOIN 
  products p ON s.product_id = p.product_id
ORDER BY 
  s.sales_month DESC;
