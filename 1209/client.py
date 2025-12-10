import module as md

# result = md.AND(0,1)
# print('x1=0', 'x2=1','AND=', result)

# md.plot_xy()

# result2 = md.AND(1,1)
# print('x1=1, x2=1, AND =', result2)

# md.sig(-10,5)

# md.rel(-10, 10)

# md.keras()


# result = md.data_process()
# print(result[0].shape, result[2].shape, result[1].shape, result[3].shape)

(train_scaled, val_scaled, train_target, val_target) = md.data_process()

#print(train_scaled.shape, train_target.shape, val_scaled.shape, val_target.shape)

model = md.model_fn()

history = md.compile_fit(model, train_scaled, train_target, val_scaled, val_target)

md.history_plot(history)

