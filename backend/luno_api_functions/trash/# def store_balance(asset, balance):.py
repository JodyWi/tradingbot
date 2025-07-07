# def store_balance(asset, balance):
#     """ Store or update balance in the database safely """
#     conn = connect_db()
#     cursor = conn.cursor()

#     try:
#         # ✅ Ensure balance is always a number
#         try:
#             clean_balance = float(balance) if balance and balance.replace('.', '', 1).isdigit() else 0.0
#         except ValueError:
#             clean_balance = 0.0  # If conversion fails, default to 0.0

#         # ✅ Check if asset exists
#         cursor.execute("SELECT id FROM balances WHERE asset = ?", (asset,))
#         existing_entry = cursor.fetchone()

#         if existing_entry:
#             cursor.execute(
#                 "UPDATE balances SET balance = ?, timestamp = CURRENT_TIMESTAMP WHERE asset = ?",
#                 (clean_balance, asset)
#             )
#         else:
#             cursor.execute(
#                 "INSERT INTO balances (asset, balance) VALUES (?, ?)",
#                 (asset, clean_balance)
#             )

#         conn.commit()
#     except Exception as e:
#         print(f"❌ Error storing balance for {asset}: {e}")
#     finally:
#         conn.close()

# def get_balance(assets=""):
#     """ Fetch balance from Luno API and store in database """
#     LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
#     if assets:
#         LUNO_API_ENDPOINT += f"?assets={assets}"

#     if not API_KEY_ID or not API_KEY_SECRET:
#         logger.error("Luno API credentials not found.")
#         return {"status": "error", "message": "Missing API credentials"}

#     credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {"Authorization": f"Basic {encoded_credentials}"}

#     response = requests.get(LUNO_API_ENDPOINT, headers=headers)

#     if response.status_code == 200:
#         balances = response.json().get("balance", [])
        
#         results = []
#         for balance in balances:
#             asset = balance.get('asset', 'UNKNOWN')
#             value = balance.get('balance', '0.0')

#             store_balance(asset, value)  # ✅ Save to DB
            
#             results.append({
#                 "Asset": asset,
#                 "Balance": float(value) if value.replace('.', '', 1).isdigit() else 0.0
#             })

#         return {"status": "success", "balances": results}
#     else:
#         logger.error(f"Failed to retrieve balances. Status code: {response.status_code}")
#         return {"status": "error", "message": "API request failed"}